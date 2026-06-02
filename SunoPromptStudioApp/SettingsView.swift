import SwiftUI

struct SettingsView: View {
    @AppStorage("EMERGENT_LLM_KEY") private var apiKey: String = ""
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
        VStack(spacing: 20) {
            VStack(spacing: 6) {
                Text("Suno Prompt Studio Settings")
                    .font(.headline)
                Text("Configure your system settings")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding(.top, 16)
            
            Divider()
            
            VStack(alignment: .leading, spacing: 8) {
                Text("Claude LLM API Key (EMERGENT_LLM_KEY)")
                    .font(.subheadline)
                    .fontWeight(.semibold)
                
                SecureField("Enter API Key (e.g. emg-llm-...)", text: $apiKey)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .frame(width: 320)
                
                Text("The API key is required to use AI and Hybrid generation modes. It is stored securely in your user account.")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(nil)
                    .fixedSize(horizontal: false, vertical: true)
                    .frame(width: 320)
            }
            .padding(.horizontal, 24)
            
            Spacer()
            
            Divider()
            
            HStack {
                Button("Cancel") {
                    presentationMode.wrappedValue.dismiss()
                }
                .keyboardShortcut(.cancelAction)
                
                Spacer()
                
                Button("Save & Apply") {
                    UserDefaults.standard.set(apiKey, forKey: "EMERGENT_LLM_KEY")
                    presentationMode.wrappedValue.dismiss()
                    
                    // Restart server to inject new key
                    AppCore.shared.reloadServerWithNewKey()
                }
                .buttonStyle(BorderedProminentButtonStyle())
                .keyboardShortcut(.defaultAction)
            }
            .padding(.horizontal, 24)
            .padding(.bottom, 16)
        }
        .frame(width: 380, height: 260)
        .background(VisualEffectView(material: .hudWindow, blendingMode: .behindWindow))
    }
}

struct VisualEffectView: NSViewRepresentable {
    let material: NSVisualEffectView.Material
    let blendingMode: NSVisualEffectView.BlendingMode
    
    func makeNSView(context: Context) -> NSVisualEffectView {
        let view = NSVisualEffectView()
        view.material = material
        view.blendingMode = blendingMode
        view.state = .active
        return view
    }
    
    func updateNSView(_ nsView: NSVisualEffectView, context: Context) {
        nsView.material = material
        nsView.blendingMode = blendingMode
    }
}
