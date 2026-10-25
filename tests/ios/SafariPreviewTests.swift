import XCTest

final class SafariPreviewTests: XCTestCase {
    let safari = XCUIApplication(bundleIdentifier: "com.apple.mobilesafari")
    let preview = "https://paul1404.github.io/QR-Redirects/01/hy-alarm?ios=ec4dbcd"

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
        XCTAssertTrue(safari.staticTexts["HY-Alarm"].exists, "Native-reader landing page is missing")
        record("01-mobile-portrait")
        safari.swipeUp()
        safari.swipeUp()
        XCTAssertTrue(link.isHittable, "PDF action disappeared after scrolling")
        record("02-mobile-after-scroll")
        XCUIDevice.shared.orientation = .landscapeLeft
        XCTAssertTrue(link.isHittable, "PDF action is not reachable in landscape")
        record("03-mobile-landscape")
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
        let title = safari.staticTexts["HY-ALARM"].firstMatch
        XCTAssertTrue(title.waitForExistence(timeout: 15), "Native PDF content did not render")
        let originalWidth = title.frame.width
        safari.webViews.firstMatch.pinch(withScale: 1.5, velocity: 1)
        XCTAssertGreaterThan(title.frame.width, originalWidth * 1.1, "Native PDF zoom did not enlarge the content")
        record("05-direct-pdf-zoomed")
        // Verify the last page is reachable, not just that the first page loads.
        let lastPage = safari.staticTexts["10 WARTUNGSPROTOKOLL"].firstMatch
        let pageIndicator = safari.staticTexts["12 of 12"].firstMatch
        for _ in 0..<40 {
            if pageIndicator.exists { break }
            safari.webViews.firstMatch.swipeUp(velocity: .slow)
        }
        record("06-direct-pdf-scroll-position")
        XCTAssertTrue(pageIndicator.waitForExistence(timeout: 10), "Safari did not reach page 12")
        XCTAssertTrue(pageIndicator.frame.intersects(safari.frame), "Last-page indicator is not on screen")
        XCTAssertTrue(lastPage.exists, "The original manual's final-page content is missing")
        record("06-direct-pdf-page-12")
        XCUIDevice.shared.orientation = .landscapeLeft
        record("07-direct-pdf-landscape")
        XCUIDevice.shared.orientation = .portrait
    }
}
