import XCTest

final class SafariPreviewTests: XCTestCase {
    let safari = XCUIApplication(bundleIdentifier: "com.apple.mobilesafari")
    let preview = "https://paul1404.github.io/QR-Redirects/01/hy-alarm"

    func record(_ name: String) {
        let screenshot = XCTAttachment(screenshot: XCUIScreen.main.screenshot())
        screenshot.name = name
        screenshot.lifetime = .keepAlways
        add(screenshot)
        let tree = XCTAttachment(string: safari.debugDescription)
        tree.name = name + "-accessibility"
        tree.lifetime = .keepAlways
        add(tree)
    }

    func address() -> XCUIElement {
        let fields = safari.textFields
        let url = fields["URL"]
        if url.exists { return url }
        let address = fields["Address"]
        if address.exists { return address }
        return fields.firstMatch
    }

    func navigate(_ url: String) {
        let field = address()
        XCTAssertTrue(field.waitForExistence(timeout: 15), "Safari address field missing")
        field.tap()
        field.press(forDuration: 1)
        let selectAll = safari.menuItems["Select All"]
        if selectAll.waitForExistence(timeout: 2) { selectAll.tap() }
        // The address bar selects its URL on focus in Safari.
        field.typeText(url + "\n")
    }

    func testLiveManualInSafari() {
        continueAfterFailure = false
        XCUIDevice.shared.orientation = .portrait
        safari.launch()
        for _ in 0..<3 {
            let welcome = safari.buttons["Continue"]
            if welcome.waitForExistence(timeout: 2) { welcome.tap() }
        }
        // The workflow opens the preview before starting XCTest.
        var link = safari.links["PDF in neuem Tab öffnen"]
        if !link.waitForExistence(timeout: 20) { navigate(preview) }
        XCTAssertTrue(link.waitForExistence(timeout: 30), "Live manual fallback link missing")
        XCTAssertTrue(link.isHittable, "PDF link is not reachable in portrait")
        XCTAssertGreaterThanOrEqual(link.frame.minX, 0)
        XCTAssertLessThanOrEqual(link.frame.maxX, safari.frame.width + 1)
        record("01-embedded-portrait")
        safari.swipeUp()
        safari.swipeUp()
        record("02-embedded-after-scroll")
        XCUIDevice.shared.orientation = .landscapeLeft
        record("03-embedded-landscape")
        XCUIDevice.shared.orientation = .portrait
        // Tapping a web link scrolls it into view if needed.
        link = safari.links["PDF in neuem Tab öffnen"]
        link.tap()
        // Wait for the original HTML link to disappear from the active tab.
        let openedPDF = NSPredicate { _, _ in !self.safari.links["PDF in neuem Tab öffnen"].exists }
        expectation(for: openedPDF, evaluatedWith: safari)
        waitForExpectations(timeout: 30)
        record("04-direct-pdf-portrait")
        let field = address()
        field.tap()
        let url = field.value as? String ?? ""
        XCTAssertTrue(url.contains("/01/pdf/Kundenanleitung_HY_Alarm.pdf"), "Direct link did not open the original PDF: \(url)")
        field.typeText("\n")
        // Exercise native document scrolling and preserve screenshots for visual review.
        for _ in 0..<14 { safari.swipeUp() }
        record("05-direct-pdf-after-scroll")
        XCUIDevice.shared.orientation = .landscapeLeft
        record("06-direct-pdf-landscape")
        XCUIDevice.shared.orientation = .portrait
    }
}
