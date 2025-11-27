import pytest
from playwright.sync_api import Page, expect
import time
import re

class TestLibraryManagementE2E:
    """Browser-based End-to-End Tests for Library Management System"""
    
    BASE_URL = "http://localhost:5000"
    
    def test_add_book_and_verify_catalog(self, page: Page):
        """
        Test user flow: Add a new book → Verify it appears in catalog
        Covers requirements i and ii
        """
        print(" Starting test: Add book and verify catalog")
        
        # Navigate to the application
        page.goto(self.BASE_URL)
        print(" Navigated to application homepage")
        
        # Wait for page to load
        page.wait_for_load_state('networkidle')
        
        # Click on Add Book navigation
        page.click("text=➕ Add Book")
        print(" Clicked Add Book navigation")
        
        # Wait for add book page to load
        page.wait_for_load_state('networkidle')
        
        # Fill in book details
        page.fill("input[name='title']", "The Great Gatsby")
        page.fill("input[name='author']", "F. Scott Fitzgerald")
        page.fill("input[name='isbn']", "9780743273565")
        page.fill("input[name='total_copies']", "3")
        print(" Filled book details")
        
        # Submit the form
        page.click("button[type='submit']")
        print(" Submitted form")
        
        # Wait for response
        page.wait_for_load_state('networkidle')
        
        # Verify success message appears
        expect(page.locator(".flash-success")).to_be_visible()
        expect(page.locator(".flash-success")).to_contain_text(re.compile(r'success|added', re.IGNORECASE))
        print(" Verified success message appears")
        
        # Navigate to catalog page
        page.click("text=📖 Catalog")
        print(" Navigated to catalog page")
        
        # Wait for catalog to load
        page.wait_for_load_state('networkidle')
        
        # Verify the book appears in the catalog with all details
        expect(page.locator("table")).to_be_visible()
        expect(page.locator("tbody")).to_contain_text("The Great Gatsby")
        expect(page.locator("tbody")).to_contain_text("F. Scott Fitzgerald")
        expect(page.locator("tbody")).to_contain_text("9780743273565")
        print(" Verified book appears in catalog with all details")

    def test_borrow_book_workflow(self, page: Page):
        """
        Test user flow: Navigate to borrow → Borrow book with patron ID → Verify confirmation
        Covers requirements iii, iv, and v
        """
        print(" Starting test: Borrow book workflow")
        
        
        # Navigate to catalog page (where borrow functionality exists)
        page.goto(f"{self.BASE_URL}/catalog")
        page.wait_for_load_state('networkidle')
        print(" Navigated to catalog page")
        
        # Verify we're on a page with book listings
        expect(page.locator("table")).to_be_visible()
        expect(page.locator("tbody")).to_be_visible()
        print(" Verified book catalog is visible")
        
        # Find the book in the table
        book_row = page.locator("tr:has-text('To Kill a Mockingbird')")
        expect(book_row).to_be_visible()
        print(" Found the test book in catalog")
        
        # Fill patron ID in the specific row
        patron_input = book_row.locator("input[name='patron_id']")
        expect(patron_input).to_be_visible()
        patron_input.fill("123456")
        print(" Filled patron ID: 123456")
        
        # Click the borrow button in the specific row
        borrow_button = book_row.locator("button:has-text('Borrow')")
        expect(borrow_button).to_be_visible()
        borrow_button.click()
        print(" Clicked borrow button")
        
        # Wait for borrow to process
        page.wait_for_load_state('networkidle')
        
        # Verify borrow confirmation message appears
        expect(page.locator(".flash-success")).to_be_visible()
        expect(page.locator(".flash-success")).to_contain_text(re.compile(r'success|borrowed', re.IGNORECASE))
        print("Verified borrow confirmation message appears")

    def test_complete_user_journey(self, page: Page):
        """
        Complete realistic user journey covering multiple workflows
        """
        print(" Starting test: Complete user journey")
        
        # Use unique data to avoid conflicts
        unique_id = str(int(time.time()))[-6:]
        test_book = {
            'title': f'Journey Test Book {unique_id}',
            'author': f'Journey Author {unique_id}',
            'isbn': f'978{unique_id}0000',
            'total_copies': '1',
            'patron_id': f'99{unique_id}'
        }
        
        # 1. Add a new book
        page.goto(f"{self.BASE_URL}/add_book")
        page.wait_for_load_state('networkidle')
        
        page.fill("input[name='title']", test_book['title'])
        page.fill("input[name='author']", test_book['author'])
        page.fill("input[name='isbn']", test_book['isbn'])
        page.fill("input[name='total_copies']", test_book['total_copies'])
        page.click("button[type='submit']")
        
        # Wait for add to complete
        page.wait_for_load_state('networkidle')
        print(" Step 1: Book added successfully")
        
        # 2. Verify book appears in catalog
        page.goto(f"{self.BASE_URL}/catalog")
        page.wait_for_load_state('networkidle')
        
        expect(page.locator("table")).to_be_visible()
        expect(page.locator("tbody")).to_contain_text(test_book['title'])
        expect(page.locator("tbody")).to_contain_text(test_book['author'])
        print(" Step 2: Book verified in catalog")
        
        # 3. Borrow the book - find the specific row
        book_row = page.locator(f"tr:has-text('{test_book['title']}')")
        patron_input = book_row.locator("input[name='patron_id']")
        patron_input.fill(test_book['patron_id'])
        
        borrow_button = book_row.locator("button:has-text('Borrow')")
        borrow_button.click()
        
        # Wait for borrow to complete
        page.wait_for_load_state('networkidle')
        
        # Verify borrow success
        expect(page.locator(".flash-success")).to_be_visible()
        expect(page.locator(".flash-success")).to_contain_text(re.compile(r'success|borrowed', re.IGNORECASE))
        print(" Step 3: Book borrowed successfully")
        
        print(" Complete user journey test finished successfully")

    def test_ui_elements_visibility(self, page: Page):
        """
        Additional test: Verify all expected UI elements appear
        """
        print(" Starting test: UI elements visibility")
        
        # Navigate to application
        page.goto(self.BASE_URL)
        page.wait_for_load_state('networkidle')
        
        # Verify navigation elements exist
        expect(page.locator("text=➕ Add Book")).to_be_visible()
        expect(page.locator("text=📖 Catalog")).to_be_visible()
        expect(page.locator("text=↩️ Return Book")).to_be_visible()
        print("✅ Verified navigation elements are visible")
        
        # Navigate to add book page and verify form elements
        page.click("text=➕ Add Book")
        page.wait_for_load_state('networkidle')
        
        expect(page.locator("input[name='title']")).to_be_visible()
        expect(page.locator("input[name='author']")).to_be_visible()
        expect(page.locator("input[name='isbn']")).to_be_visible()
        expect(page.locator("input[name='total_copies']")).to_be_visible()
        expect(page.locator("button[type='submit']")).to_be_visible()
        print("✅ Verified add book form elements are visible")
        
        # Navigate to return page and verify form elements
        page.click("text=↩️ Return Book")
        page.wait_for_load_state('networkidle')
        
        expect(page.locator("input[name='patron_id']")).to_be_visible()
        expect(page.locator("input[name='book_id']")).to_be_visible()
        expect(page.locator("button[type='submit']")).to_be_visible()
        print("✅ Verified return book form elements are visible")
        
        # Navigate to catalog and verify table and borrow elements
        page.click("text=📖 Catalog")
        page.wait_for_load_state('networkidle')
        
        expect(page.locator("table")).to_be_visible()
        expect(page.locator("tbody")).to_be_visible()
        expect(page.locator("input[name='patron_id']").first).to_be_visible()
        expect(page.locator("button:has-text('Borrow')").first).to_be_visible()
        print("✅ Verified catalog and borrow elements are visible")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context for all tests
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }

@pytest.fixture(autouse=True)
def setup_page(page: Page):
    """
    Setup for each test with increased timeout and better error handling
    """
    page.set_default_timeout(15000)  # Increased to 15 seconds
    page.set_default_navigation_timeout(15000)
    yield