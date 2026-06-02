import SwiftUI

struct ContentView: View {
    @StateObject private var core = AppCore.shared
    @State private var showLogs = false
    @State private var isShowingSettings = false
    
    var body: some View {
        VStack(spacing: 0) {
            switch core.state {
            case .checkingSetup, .creatingVenv, .installingRequirements, .startingServer:
                VStack(spacing: 20) {
                    ProgressView()
                        .scaleEffect(1.2)
                        .padding(.bottom, 8)
                    
                    Text(statusMessage(for: core.state))
                        .font(.headline)
                        .foregroundColor(.primary)
                    
                    ProgressView(value: core.setupProgress)
                        .frame(width: 300)
                        .accentColor(.blue)
                    
                    Button("Show Environment Console Logs") {
                        showLogs.toggle()
                    }
                    .buttonStyle(LinkButtonStyle())
                    .font(.caption)
                    .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(VisualEffectView(material: .windowBackground, blendingMode: .behindWindow))
                
            case .ready(let url):
                WebView(url: url)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                
            case .error(let message):
                VStack(spacing: 20) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .font(.system(size: 48))
                        .foregroundColor(.orange)
                    
                    Text("Error Launching Application")
                        .font(.title3)
                        .fontWeight(.bold)
                    
                    Text(message)
                        .font(.body)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                        .frame(width: 420)
                    
                    HStack(spacing: 12) {
                        Button("Retry Setup") {
                            core.setupAndStart()
                        }
                        .buttonStyle(BorderedProminentButtonStyle())
                        
                        Button("Configure Key") {
                            isShowingSettings.toggle()
                        }
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(VisualEffectView(material: .windowBackground, blendingMode: .behindWindow))
            }
            
            // Collapsible Logs Tray at the bottom
            if showLogs || isSetupState(core.state) {
                VStack(spacing: 0) {
                    Divider()
                    HStack {
                        Text("Backend Server Console Logs")
                            .font(.caption)
                            .fontWeight(.semibold)
                            .foregroundColor(.secondary)
                            .padding(.leading)
                        
                        Spacer()
                        
                        Button(action: {
                            showLogs.toggle()
                        }) {
                            Image(systemName: showLogs ? "chevron.down" : "chevron.up")
                                .font(.caption)
                                .padding(.horizontal, 8)
                        }
                        .buttonStyle(PlainButtonStyle())
                        .padding(.trailing)
                    }
                    .frame(height: 28)
                    .background(Color(NSColor.windowBackgroundColor))
                    
                    if showLogs {
                        ScrollView {
                            Text(core.logOutput)
                                .font(.system(.caption, design: .monospaced))
                                .foregroundColor(.primary)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .padding(8)
                        }
                        .frame(height: 180)
                        .background(Color(NSColor.textBackgroundColor))
                    }
                }
            }
        }
        .sheet(isPresented: $isShowingSettings) {
            SettingsView()
        }
        .onAppear {
            core.setupAndStart()
        }
    }
    
    private func isSetupState(_ state: AppCore.AppState) -> Bool {
        switch state {
        case .ready:
            return false
        default:
            return true
        }
    }
    
    private func statusMessage(for state: AppCore.AppState) -> String {
        switch state {
        case .checkingSetup:
            return "Verifying local environment..."
        case .creatingVenv:
            return "Creating Python virtual environment (.venv)..."
        case .installingRequirements:
            return "Installing application dependencies..."
        case .startingServer:
            return "Starting FastAPI server..."
        default:
            return "Loading..."
        }
    }
}
