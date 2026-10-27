import XCTest

final class SafariPreviewTests: XCTestCase {
    let safari = XCUIApplication(bundleIdentifier: "com.apple.mobilesafari")

    func record(_ name: String) {
        // Fetch the settled accessibility snapshot before capturing rotation frames.
        let tree = XCTAttachment(string: safari.debugDescription)
        tree.name = name + "-accessibility"
        tree.lifetime = .keepAlways
        add(tree)
        let screenshot = XCTAttachment(screenshot: XCUIScreen.main.screenshot())
        screenshot.name = name
        screenshot.lifetime = .keepAlways
        add(screenshot)
    }

    func address() -> XCUIElement {
        if safari.textFields["URL"].exists { return safari.textFields["URL"] }
        if safari.textFields["Address"].exists { return safari.textFields["Address"] }
        return safari.textFields.firstMatch
    }

    func testNativePDFReading() {
        continueAfterFailure = false
        XCUIDevice.shared.orientation = .portrait
        safari.launch()
        for _ in 0..<3 {
            let welcome = safari.buttons["Continue"]
            if welcome.waitForExistence(timeout: 2) { welcome.tap() }
        }
        // Open via Safari UI after launch rather than racing simctl during cold boot.
        let entry = address()
        entry.tap()
        entry.typeText("PREVIEW_ENTRY_URL\n")
        let title = safari.staticTexts["HY-ALARM"].firstMatch
        XCTAssertTrue(title.waitForExistence(timeout: 60), "The PDF did not open automatically")
        // PDF reading collapses Safari's address field into a non-hittable AX item.
        // On this fixed iPhone 16 portrait layout, open the visible bottom omnibar.
        let field = safari.textFields["URL"].firstMatch
        for _ in 0..<3 {
            safari.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.935)).tap()
            if field.waitForExistence(timeout: 3) { break }
        }
        XCTAssertTrue(field.exists, "Full address field did not open")
        let url = field.value as? String ?? ""
        XCTAssertTrue(url.contains("/01/pdf/EXPECTED_PDF_NAME"), "Unexpected document address: \(url)")
        XCTAssertFalse(url.contains("v="), "Manual access should not require a version parameter")
        field.typeText("\n")
        XCTAssertTrue(title.waitForExistence(timeout: 30))
        record("01-native-pdf-portrait")

        let originalWidth = title.frame.width
        safari.webViews.firstMatch.pinch(withScale: 1.5, velocity: 1)
        XCTAssertGreaterThan(title.frame.width, originalWidth * 1.1, "Native PDF zoom did not enlarge the content")
        record("02-native-pdf-zoomed")

        let pageIndicator = safari.staticTexts["12 of 12"].firstMatch
        var reachedLastPage = false
        for _ in 0..<40 {
            if pageIndicator.exists {
                reachedLastPage = true
                print("Verified native Safari page indicator: 12 of 12")
                break
            }
            safari.webViews.firstMatch.swipeUp(velocity: .slow)
        }
        XCTAssertTrue(reachedLastPage, "Safari did not reach page 12")
        XCTAssertTrue(safari.staticTexts["10 WARTUNGSPROTOKOLL"].exists)
        record("03-native-pdf-page-12")

        XCUIDevice.shared.orientation = .landscapeLeft
        XCTAssertGreaterThan(safari.frame.width, safari.frame.height)
        record("04-native-pdf-landscape")
        XCUIDevice.shared.orientation = .portrait
    }
}
