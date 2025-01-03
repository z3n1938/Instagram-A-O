import instaloader
import requests
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Function to fetch Reels Links in bulk
def fetch_reels_links_bulk(usernames):
    L = instaloader.Instaloader()

    for username in usernames:
        profile = instaloader.Profile.from_username(L.context, username)

        reels_links = []
        for post in profile.get_posts():
            if post.typename == 'GraphVideo':  # Reels are of type 'GraphVideo'
                reels_links.append(post.url)

        if reels_links:
            filename = f"{username}_reels_links.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"Reels Links for @{username}:\n")
                for link in reels_links:
                    file.write(f"{link}\n")
            print(Fore.MAGENTA + f"Reels links saved to {filename}")
        else:
            print(Fore.YELLOW + f"No reels found for @{username}.")

# Function to scrape Profile Data in bulk
def scrape_profile_data_bulk(usernames):
    L = instaloader.Instaloader()

    for username in usernames:
        profile = instaloader.Profile.from_username(L.context, username)

        profile_data = {
            'Username': profile.username,
            'Full Name': profile.full_name,
            'Bio': profile.biography,
            'Followers': profile.followers,
            'Following': profile.followees,
            'Posts': profile.mediacount,
            'Is Verified': profile.is_verified,
            'Profile Picture URL': profile.profile_pic_url,
        }

        filename = f"{username}_profile_data.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Profile Data for @{username}:\n")
            for key, value in profile_data.items():
                file.write(f"{key}: {value}\n")
        print(Fore.CYAN + f"Profile data saved to {filename}")

# Function to download videos from a list of Instagram post URLs in bulk
def download_videos_bulk(post_urls):
    L = instaloader.Instaloader()

    for post_url in post_urls:
        shortcode = post_url.split("/")[-2]

        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            video_url = post.url
            video_data = requests.get(video_url)

            filename = f"{shortcode}.mp4"
            with open(filename, 'wb') as file:
                file.write(video_data.content)

            # Save a confirmation message to a text file
            download_log = f"Video {shortcode} downloaded as {filename}"
            with open(f"{shortcode}_download_log.txt", 'w', encoding='utf-8') as log_file:
                log_file.write(download_log)

            print(Fore.GREEN + download_log)
        except Exception as e:
            print(Fore.RED + f"Error occurred for {post_url}: {e}")

# Function to download profile pictures in bulk
def download_profile_pictures_bulk(usernames):
    L = instaloader.Instaloader()

    for username in usernames:
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            profile_pic_url = profile.profile_pic_url
            profile_pic_data = requests.get(profile_pic_url)

            # Saving the profile picture
            filename = f"{username}_profile_pic.jpg"
            with open(filename, 'wb') as file:
                file.write(profile_pic_data.content)

            print(Fore.YELLOW + f"Profile picture of {username} saved as {filename}")
        except Exception as e:
            print(Fore.RED + f"Error occurred for {username}: {e}")

# Main function to allow user to choose and perform bulk operations
def main():
    print(Fore.WHITE + Style.BRIGHT + "Select a task:")  # White for task selection heading
    print(Fore.GREEN + "[1] Fetch Reels Links (Bulk)")
    print(Fore.GREEN + "[2] Scrape Profile Data (Bulk)")
    print(Fore.GREEN + "[3] Download Videos from Links (Bulk)")
    print(Fore.GREEN + "[4] Download Profile Pictures (Bulk)")
    choice = input(Fore.RED + "Enter your choice: ").strip()  # Red for user input prompt

    if choice == "1":
        usernames = input(Fore.BLUE + "Enter Instagram usernames (comma separated): ").split(",")
        usernames = [username.strip() for username in usernames]  # Clean up spaces
        fetch_reels_links_bulk(usernames)
    elif choice == "2":
        usernames = input(Fore.BLUE + "Enter Instagram usernames (comma separated): ").split(",")
        usernames = [username.strip() for username in usernames]  # Clean up spaces
        scrape_profile_data_bulk(usernames)
    elif choice == "3":
        post_urls = input(Fore.BLUE + "Enter Instagram post URLs (comma separated): ").split(",")
        post_urls = [url.strip() for url in post_urls]  # Clean up spaces
        download_videos_bulk(post_urls)
    elif choice == "4":
        usernames = input(Fore.BLUE + "Enter Instagram usernames (comma separated): ").split(",")
        usernames = [username.strip() for username in usernames]  # Clean up spaces
        download_profile_pictures_bulk(usernames)
    else:
        print(Fore.RED + "Invalid choice!")

if __name__ == "__main__":
    main()
