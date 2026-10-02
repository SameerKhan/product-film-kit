// ocr.swift <png...>: prints "<file>\t<recognised text joined by |>" using macOS Vision (on-device).
// Build once: mkdir -p build && swiftc -O scripts/ocr.swift -o build/ocr
// Exit 2 if any image could not be read or recognised, so a gate never mistakes an error for "text absent".
import Foundation
import Vision
import AppKit
var failed = false
for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("\(path)\tREAD-FAIL"); failed = true; continue }
    let req = VNRecognizeTextRequest(); req.recognitionLevel = .accurate; req.usesLanguageCorrection = false
    do { try VNImageRequestHandler(cgImage: cg).perform([req]) } catch { print("\(path)\tOCR-FAIL"); failed = true; continue }
    let txt = (req.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "|")
    print("\(path)\t\(txt)")
}
exit(failed ? 2 : 0)
