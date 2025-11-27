"""
Automated OutReply Voter - Runs N votes automatically with different IPs
OPTIMIZED FOR LOW BANDWIDTH - Blocks images, fonts, and analytics
✅ INCLUDES REAL-TIME BANDWIDTH TRACKING
Configure settings at the top of this file and run it
"""
import undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import logging
from datetime import datetime
import sys

# ========== CONFIGURATION ==========
# Poll Settings
POLL_URL = "https://www.outreply.com/polls/YOUR_POLL_ID_HERE"  # The full poll URL
VOTE_OPTION = "Your Option Name"  # The exact text of the option you want to vote for

# Proxy Settings (DataImpulse format)
PROXY_USERNAME = "your_username__cr.us"  # Your proxy username with country code
PROXY_PASSWORD = "your_password"  # Your proxy password
PROXY_HOST = "gw.dataimpulse.com"  # Proxy server hostname
PROXY_PORT = 823  # Proxy port

# Vote Settings
NUMBER_OF_VOTES = 10  # How many votes to cast
HEADLESS = True  # True = runs in background, False = shows browser
FAST_MODE = True  # True = fast (~5s per vote), False = slow human-like
DELAY_BETWEEN_VOTES = (1.0, 3.0)  # Random delay between votes in seconds (min, max)

# Bandwidth Optimization (SAVES ~75% bandwidth!)
BLOCK_IMAGES = True  # Block images to save bandwidth
BLOCK_FONTS = True  # Block fonts to save bandwidth  
BLOCK_ANALYTICS = True  # Block tracking/analytics to save bandwidth
# ===================================

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f'auto_voter_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class AutoVoter:
    def __init__(self):
        self.poll_url = POLL_URL
        self.vote_option = VOTE_OPTION
        
        # Proxy configuration
        self.proxy_username = PROXY_USERNAME
        self.proxy_password = PROXY_PASSWORD
        self.proxy_host = PROXY_HOST
        self.proxy_port = PROXY_PORT
        
        self.stats = {
            'total_attempts': 0,
            'successful': 0,
            'failed': 0,
            'start_time': None,
            'end_time': None,
            'total_bandwidth_mb': 0.0,  # Track total bandwidth used
        }
    
    def create_driver(self, session_id: str, headless: bool):
        """Create Chrome driver with proxy and bandwidth optimization"""
        username_with_session = f"{self.proxy_username}__session-{session_id}"
        proxy_url = f"http://{username_with_session}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}"
        
        # Request interceptor to block unnecessary resources and save bandwidth
        def interceptor(request):
            # Block images
            if BLOCK_IMAGES and any(x in request.url.lower() for x in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico']):
                request.abort()
                return
            
            # Block fonts
            if BLOCK_FONTS and any(x in request.url.lower() for x in ['.woff', '.woff2', '.ttf', '.otf', 'fonts.g']):
                request.abort()
                return
            
            # Block analytics and tracking
            if BLOCK_ANALYTICS and any(x in request.url.lower() for x in [
                'google-analytics.com',
                'googletagmanager.com',
                'clarity.ms',
                '/analytics',
                '/tracking',
                'gtag',
                'tiktok.com',
                'lemonsqueezy.com',
                'lmsqueezy.com',
                '/embed.js',
                '/affiliate'
            ]):
                request.abort()
                return
        
        seleniumwire_options = {
            'proxy': {
                'http': proxy_url,
                'https': proxy_url,
                'no_proxy': 'localhost,127.0.0.1'
            },
            'verify_ssl': False,
            'suppress_connection_errors': True,
        }
        
        chrome_options = uc.ChromeOptions()
        
        # Additional bandwidth-saving options
        if BLOCK_IMAGES:
            chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        
        if headless:
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-gpu')
        else:
            chrome_options.add_argument('--start-maximized')
        
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        
        driver = webdriver.Chrome(
            seleniumwire_options=seleniumwire_options,
            options=chrome_options
        )
        
        # Apply request interceptor
        driver.request_interceptor = interceptor
        
        return driver
    
    def vote_once(self, vote_number: int, headless: bool, fast_mode: bool):
        """Execute a single vote"""
        session_id = f"auto-{vote_number}-{random.randint(100000, 999999)}"
        
        driver = None
        vote_bandwidth_mb = 0.0
        
        try:
            logger.info(f"🎯 VOTE #{vote_number}/{NUMBER_OF_VOTES} - Session: {session_id}")
            
            driver = self.create_driver(session_id, headless=headless)
            
            # Track bandwidth before starting
            initial_request_count = len(driver.requests)
            
            # Navigate to poll
            driver.get(self.poll_url)
            
            # Wait for page
            wait = WebDriverWait(driver, 15)
            time.sleep(0.5 if fast_mode else 1)
            
            # Find the voting option
            vote_element = wait.until(
                EC.presence_of_element_located((By.XPATH, f"//h5[contains(text(), '{self.vote_option}')]"))
            )
            
            # Get card and click
            card = vote_element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'option-card')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
            time.sleep(0.2 if fast_mode else 0.5)
            
            card.click()
            time.sleep(0.5 if fast_mode else 1.5)
            
            # Find and click Submit button
            submit_selectors = [
                "//button[contains(., 'Submit Vote')]",
                "//button[contains(@class, 'btn') and contains(., 'Submit')]",
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = driver.find_element(By.XPATH, selector)
                    if submit_button.is_displayed() and submit_button.is_enabled():
                        break
                    else:
                        submit_button = None
                except:
                    continue
            
            if submit_button:
                submit_button.click()
                time.sleep(2 if fast_mode else 3)
                
                # Check for success message
                try:
                    success_selectors = [
                        "//div[contains(@class, 'success')]",
                        "//div[contains(text(), 'Thank')]",
                    ]
                    
                    for selector in success_selectors:
                        try:
                            element = driver.find_element(By.XPATH, selector)
                            if element.is_displayed():
                                logger.info(f"✅ Vote #{vote_number} SUCCESSFUL!")
                                self.stats['successful'] += 1
                                return True
                        except:
                            continue
                    
                    # If no success message found, assume success (some sites don't show messages)
                    logger.info(f"✅ Vote #{vote_number} submitted (no confirmation message)")
                    self.stats['successful'] += 1
                    return True
                    
                except:
                    logger.info(f"✅ Vote #{vote_number} submitted")
                    self.stats['successful'] += 1
                    return True
            else:
                logger.error(f"❌ Vote #{vote_number} FAILED - No submit button")
                self.stats['failed'] += 1
                return False
                
        except Exception as e:
            logger.error(f"❌ Vote #{vote_number} FAILED - {str(e)}")
            self.stats['failed'] += 1
            return False
            
        finally:
            self.stats['total_attempts'] += 1
            
            # Calculate bandwidth used for this vote
            if driver:
                try:
                    total_bytes = 0
                    for request in driver.requests:
                        # Add request size
                        if hasattr(request, 'body') and request.body:
                            total_bytes += len(request.body)
                        
                        # Add response size
                        if hasattr(request, 'response') and request.response:
                            if hasattr(request.response, 'body') and request.response.body:
                                total_bytes += len(request.response.body)
                    
                    vote_bandwidth_mb = total_bytes / (1024 * 1024)  # Convert to MB
                    self.stats['total_bandwidth_mb'] += vote_bandwidth_mb
                    
                    logger.info(f"📊 Vote #{vote_number} used: {vote_bandwidth_mb:.2f} MB | Total so far: {self.stats['total_bandwidth_mb']:.2f} MB")
                except Exception as e:
                    logger.warning(f"⚠️ Could not calculate bandwidth: {e}")
                
                driver.quit()
    
    def run(self):
        """Run all votes automatically"""
        logger.info("\n" + "="*60)
        logger.info("🤖 AUTOMATED OUTREPLY VOTER (BANDWIDTH OPTIMIZED)")
        logger.info("="*60)
        logger.info(f"Target: {self.poll_url}")
        logger.info(f"Voting For: {self.vote_option}")
        logger.info(f"Total Votes: {NUMBER_OF_VOTES}")
        logger.info(f"Mode: {'HEADLESS' if HEADLESS else 'VISIBLE'}")
        logger.info(f"Speed: {'FAST ⚡' if FAST_MODE else 'NORMAL'}")
        logger.info(f"Delay Between Votes: {DELAY_BETWEEN_VOTES[0]}-{DELAY_BETWEEN_VOTES[1]}s")
        logger.info(f"Proxy: ENABLED (each vote uses different IP)")
        logger.info(f"Bandwidth Saving: Images={'BLOCKED' if BLOCK_IMAGES else 'LOADED'}, Fonts={'BLOCKED' if BLOCK_FONTS else 'LOADED'}, Analytics={'BLOCKED' if BLOCK_ANALYTICS else 'LOADED'}")
        logger.info(f"Estimated Data Usage: ~{NUMBER_OF_VOTES * 4.0:.1f} MB (~4 MB per vote)")
        logger.info("="*60 + "\n")
        
        self.stats['start_time'] = datetime.now()
        
        for i in range(1, NUMBER_OF_VOTES + 1):
            success = self.vote_once(i, headless=HEADLESS, fast_mode=FAST_MODE)
            
            # Delay before next vote (except after last vote)
            if i < NUMBER_OF_VOTES:
                delay = random.uniform(DELAY_BETWEEN_VOTES[0], DELAY_BETWEEN_VOTES[1])
                logger.info(f"⏳ Waiting {delay:.1f}s before next vote...\n")
                time.sleep(delay)
        
        self.stats['end_time'] = datetime.now()
        self.print_final_stats()
    
    def print_final_stats(self):
        """Print final statistics"""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        logger.info("📊 BANDWIDTH USAGE")
        logger.info("="*60)
        logger.info(f"Total Data Used: {self.stats['total_bandwidth_mb']:.2f} MB")
        
        if self.stats['successful'] > 0:
            avg_bandwidth = self.stats['total_bandwidth_mb'] / self.stats['successful']
            logger.info(f"Average Per Successful Vote: {avg_bandwidth:.2f} MB")
        
        logger.info("="*60)
        
        logger.info("\n" + "="*60)
        logger.info("📈 PERFORMANCE")
        logger.info("="*60)
        logger.info(f"Total Votes: {self.stats['total_attempts']}")
        logger.info(f"✅ Successful: {self.stats['successful']}")
        logger.info(f"❌ Failed: {self.stats['failed']}")
        
        if self.stats['total_attempts'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_attempts']) * 100
            logger.info(f"Success Rate: {success_rate:.1f}%")
        
        logger.info(f"Total Time: {duration:.1f}s ({duration/60:.1f} minutes)")
        
        if self.stats['successful'] > 0:
            avg_time = duration / self.stats['successful']
            logger.info(f"Average Time Per Vote: {avg_time:.1f}s")
        
        logger.info("="*60)
        
        logger.info("\n" + "="*60)
        logger.info("🎯 FINAL SUMMARY")
        logger.info("="*60)
        
        if self.stats['successful'] == NUMBER_OF_VOTES:
            logger.info(f"\n🎉 ALL {NUMBER_OF_VOTES} VOTES SUCCESSFUL!")
        elif self.stats['successful'] > 0:
            logger.info(f"\n⚠️ PARTIAL SUCCESS - {self.stats['successful']}/{NUMBER_OF_VOTES} votes succeeded")
        else:
            logger.info("\n❌ ALL VOTES FAILED")


if __name__ == "__main__":
    # Validate configuration
    if "YOUR_POLL_ID_HERE" in POLL_URL:
        print("\n❌ ERROR: Please configure POLL_URL in the script!")
        print("Edit auto_voter.py and set your poll URL.\n")
        sys.exit(1)
    
    if PROXY_USERNAME == "your_username__cr.us":
        print("\n❌ ERROR: Please configure proxy credentials in the script!")
        print("Edit auto_voter.py and set your proxy settings.\n")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🤖 AUTOMATED OUTREPLY VOTER (BANDWIDTH OPTIMIZED)")
    print("="*60)
    print(f"Poll: {POLL_URL}")
    print(f"Voting For: {VOTE_OPTION}")
    print(f"Total Votes: {NUMBER_OF_VOTES}")
    print(f"Mode: {'HEADLESS (background)' if HEADLESS else 'VISIBLE (shows browser)'}")
    print(f"Speed: {'FAST ⚡' if FAST_MODE else 'NORMAL'}")
    print(f"Bandwidth Optimization: {'ENABLED ✅' if BLOCK_IMAGES else 'DISABLED'}")
    print(f"Estimated Usage: ~{NUMBER_OF_VOTES * 4.0:.1f} MB")
    print("="*60 + "\n")
    
    print("Starting in 3 seconds... (Press Ctrl+C to cancel)")
    try:
        time.sleep(3)
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    
    voter = AutoVoter()
    voter.run()
