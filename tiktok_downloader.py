import subprocess
import os


def download_tiktok_profile(profile_url, cookies_file=None):
    """
    Downloads all videos and photos from a TikTok profile URL,
    with an option to use a cookies file for private accounts.
    """
    try:
        if "@" not in profile_url:
            print("❌ Error: Invalid TikTok profile URL. It should contain '@'.")
            return

        username = profile_url.split('@')[1].split('/')[0]
        download_folder = username

        print(f"✅ Username found: {username}")
        print(f"📂 Files will be saved in a folder named '{download_folder}'")

        os.makedirs(download_folder, exist_ok=True)

        # Base command with added politeness settings to avoid blocks
        command = [
            'yt-dlp',
            '--ignore-errors',
            '--sleep-requests', '1',  # Be polite, wait 1 sec between page requests
            '--sleep-interval', '2',  # Wait 2 seconds between video downloads
            '-o', f'{download_folder}/%(id)s - %(title)s.%(ext)s',
        ]

        # If a cookies file is provided, add it to the command
        if cookies_file:
            print(f"🍪 Using cookies from: {cookies_file}")
            command.extend(['--cookies', cookies_file])

        # Add the URL at the end
        command.append(profile_url)

        print("\n🚀 Starting download... This might take a while.")
        print("-----------------------------------------------------------------------")

        subprocess.run(command, check=True)

        print("-----------------------------------------------------------------------")
        print(f"🎉 Download complete! Check the '{download_folder}' folder.")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ An error occurred during download: {e}")
        print("   This can happen if the profile is private and you aren't using cookies,")
        print("   or if TikTok is blocking requests. Make sure yt-dlp is updated!")
    except FileNotFoundError:
        print("❌ Error: 'yt-dlp' not found. Is it installed and in your PATH?")
        print("   Try running: pip install --upgrade yt-dlp")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    print("--- TikTok Profile Downloader ---")

    # Check for the default cookies file
    default_cookie_path = 'tiktok-cookies.txt'
    use_cookies = False

    if os.path.exists(default_cookie_path):
        answer = input(f"🍪 Found '{default_cookie_path}'. Use it for login? (y/n): ").lower()
        if answer == 'y':
            use_cookies = True

    url = input("🔗 Please paste the TikTok profile URL and press Enter: ")

    if url:
        if use_cookies:
            download_tiktok_profile(url.strip(), cookies_file=default_cookie_path)
        else:
            download_tiktok_profile(url.strip())
    else:
        print("No URL entered. Exiting.")