import Foundation
import Combine

class AppCore: ObservableObject {
    static let shared = AppCore()
    
    enum AppState: Equatable {
        case checkingSetup
        case creatingVenv
        case installingRequirements
        case startingServer
        case ready(url: URL)
        case error(message: String)
    }
    
    @Published var state: AppState = .checkingSetup
    @Published var logOutput: String = ""
    @Published var setupProgress: Double = 0.0
    
    private var process: Process?
    private var stdoutPipe: Pipe?
    private var stderrPipe: Pipe?
    
    let projectDir = "/Users/master/.gemini/antigravity/scratch/Suno-Prompt-Studio"
    let backendDir = "/Users/master/.gemini/antigravity/scratch/Suno-Prompt-Studio/backend"
    
    private init() {}
    
    func appendLog(_ text: String) {
        DispatchQueue.main.async {
            self.logOutput += text
            // Keep log size reasonable (last 10,000 characters)
            if self.logOutput.count > 10000 {
                self.logOutput = String(self.logOutput.suffix(10000))
            }
        }
        
        // Write to persistent log file on disk inside the backend directory
        let logFilePath = "\(self.backendDir)/backend_server.log"
        if let data = text.data(using: .utf8) {
            if FileManager.default.fileExists(atPath: logFilePath) {
                if let fileHandle = try? FileHandle(forWritingTo: URL(fileURLWithPath: logFilePath)) {
                    fileHandle.seekToEndOfFile()
                    fileHandle.write(data)
                    fileHandle.closeFile()
                }
            } else {
                try? data.write(to: URL(fileURLWithPath: logFilePath))
            }
        }
    }
    
    func updateProgress(_ progress: Double) {
        DispatchQueue.main.async {
            self.setupProgress = progress
        }
    }
    
    func updateState(_ state: AppState) {
        DispatchQueue.main.async {
            self.state = state
        }
    }
    
    func setupAndStart() {
        // Run setup on a background thread so as not to freeze the UI
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            guard let self = self else { return }
            
            do {
                self.updateState(.checkingSetup)
                self.appendLog("[System] Checking environment setup...\n")
                
                let venvDir = "\(self.backendDir)/.venv"
                let venvExists = FileManager.default.fileExists(atPath: venvDir)
                
                if !venvExists {
                    self.updateState(.creatingVenv)
                    self.updateProgress(0.2)
                    self.appendLog("[System] Python virtual environment (.venv) not found. Creating one...\n")
                    try self.runCommandSync(executable: "/usr/bin/python3", arguments: ["-m", "venv", ".venv"], currentDirectory: self.backendDir)
                }
                
                let pipExecutable = "\(venvDir)/bin/pip"
                let requirementsExists = FileManager.default.fileExists(atPath: "\(self.backendDir)/requirements.txt")
                
                if !venvExists && requirementsExists {
                    self.updateState(.installingRequirements)
                    self.updateProgress(0.5)
                    self.appendLog("[System] Installing backend dependencies from requirements.txt...\n")
                    try self.runCommandSync(executable: pipExecutable, arguments: ["install", "-r", "requirements.txt"], currentDirectory: self.backendDir)
                }
                
                self.updateProgress(0.8)
                self.updateState(.startingServer)
                self.appendLog("[System] Starting local FastAPI backend server...\n")
                
                try self.startBackendServer()
                
            } catch {
                self.appendLog("[Error] Setup failed: \(error.localizedDescription)\n")
                self.updateState(.error(message: "Setup failed: \(error.localizedDescription)"))
            }
        }
    }
    
    private func runCommandSync(executable: String, arguments: [String], currentDirectory: String) throws {
        let task = Process()
        task.executableURL = URL(fileURLWithPath: executable)
        task.arguments = arguments
        task.currentDirectoryURL = URL(fileURLWithPath: currentDirectory)
        
        let pipe = Pipe()
        task.standardOutput = pipe
        task.standardError = pipe
        
        try task.run()
        
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        if let output = String(data: data, encoding: .utf8), !output.isEmpty {
            self.appendLog(output)
        }
        
        task.waitUntilExit()
        
        if task.terminationStatus != 0 {
            throw NSError(domain: "AppCoreCommandError", code: Int(task.terminationStatus), userInfo: [NSLocalizedDescriptionKey: "Command failed with status \(task.terminationStatus)"])
        }
    }
    
    private func startBackendServer() throws {
        // Stop any running instance first
        stop()
        
        let port = 8000
        let venvDir = "\(backendDir)/.venv"
        let uvicornPath = "\(venvDir)/bin/uvicorn"
        
        let task = Process()
        task.executableURL = URL(fileURLWithPath: uvicornPath)
        task.arguments = ["server:app", "--host", "127.0.0.1", "--port", String(port)]
        task.currentDirectoryURL = URL(fileURLWithPath: backendDir)
        
        // Pass the API Key from UserDefaults as an environment variable
        var env = ProcessInfo.processInfo.environment
        if let apiKey = UserDefaults.standard.string(forKey: "EMERGENT_LLM_KEY"), !apiKey.isEmpty {
            env["EMERGENT_LLM_KEY"] = apiKey
            appendLog("[System] Injecting saved EMERGENT_LLM_KEY into backend environment.\n")
        } else {
            appendLog("[System] Warning: No EMERGENT_LLM_KEY configured. Prompt generation will fail until configured in Settings.\n")
        }
        
        // Inject SQLite database config (deactivates MongoDB)
        env["MONGO_URL"] = ""
        task.environment = env
        
        let stdout = Pipe()
        let stderr = Pipe()
        task.standardOutput = stdout
        task.standardError = stderr
        
        self.process = task
        self.stdoutPipe = stdout
        self.stderrPipe = stderr
        
        // Read output asynchronously
        stdout.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            if !data.isEmpty, let output = String(data: data, encoding: .utf8) {
                self?.appendLog(output)
            }
        }
        
        stderr.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            if !data.isEmpty, let output = String(data: data, encoding: .utf8) {
                self?.appendLog(output)
            }
        }
        
        try task.run()
        appendLog("[System] uvicorn server started on pid \(task.processIdentifier)\n")
        
        // Poll the health endpoint until it is ready
        pollHealthEndpoint(url: URL(string: "http://127.0.0.1:\(port)/")!, port: port)
    }
    
    private func pollHealthEndpoint(url: URL, port: Int) {
        DispatchQueue.global(qos: .background).async { [weak self] in
            guard let self = self else { return }
            
            var attempts = 0
            let maxAttempts = 40
            
            while attempts < maxAttempts {
                attempts += 1
                self.appendLog("[System] Polling health check (attempt \(attempts)/\(maxAttempts))...\n")
                
                var request = URLRequest(url: url.appendingPathComponent("api/"))
                request.timeoutInterval = 1.0
                
                let semaphore = DispatchSemaphore(value: 0)
                var success = false
                
                let sessionTask = URLSession.shared.dataTask(with: request) { _, response, _ in
                    if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                        success = true
                    }
                    semaphore.signal()
                }
                sessionTask.resume()
                _ = semaphore.wait(timeout: .now() + 1.2)
                
                if success {
                    self.appendLog("[System] Backend is healthy and ready!\n")
                    self.updateProgress(1.0)
                    self.updateState(.ready(url: URL(string: "http://127.0.0.1:\(port)")!))
                    return
                }
                
                Thread.sleep(forTimeInterval: 0.5)
            }
            
            self.updateState(.error(message: "Backend server failed to start within the timeout period. Please check the logs."))
        }
    }
    
    func reloadServerWithNewKey() {
        appendLog("[System] Settings updated. Restarting backend to apply new configuration...\n")
        setupAndStart()
    }
    
    func stop() {
        if let process = self.process, process.isRunning {
            appendLog("[System] Stopping backend server (pid \(process.processIdentifier))...\n")
            process.terminate()
            process.waitUntilExit()
            appendLog("[System] Backend server stopped successfully.\n")
        }
        
        self.stdoutPipe?.fileHandleForReading.readabilityHandler = nil
        self.stderrPipe?.fileHandleForReading.readabilityHandler = nil
        self.process = nil
        self.stdoutPipe = nil
        self.stderrPipe = nil
    }
}
