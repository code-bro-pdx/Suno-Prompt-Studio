import SwiftUI
import AppKit

class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationWillTerminate(_ notification: Notification) {
        // Stop the FastAPI backend subprocess cleanly when quitting the app
        AppCore.shared.stop()
    }
    
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        // Terminate application when the last window is closed
        return true
    }
}

@main
struct SunoPromptStudioApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    @State private var isShowingSettings = false
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 1024, minHeight: 700)
                .sheet(isPresented: $isShowingSettings) {
                    SettingsView()
                }
        }
        .windowStyle(.titleBar)
        .commands {
            // Custom application menu commands
            CommandGroup(replacing: .appInfo) {
                Button("About Suno Prompt Studio") {
                    NSApplication.shared.orderFrontStandardAboutPanel(
                        options: [
                            .credits: "Built natively using SwiftUI wrapping the Suno Prompt Studio frontend and FastAPI backend.",
                            .version: "1.0.0"
                        ]
                    )
                }
                
                Divider()
                
                Button("Settings...") {
                    isShowingSettings = true
                }
                .keyboardShortcut(",", modifiers: .command)
                
                Divider()
            }
        }
    }
}
