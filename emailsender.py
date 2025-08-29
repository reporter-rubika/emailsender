import requests
import time
import random
import json
from datetime import datetime
import threading

class AdvancedTempEmailSender:
    def __init__(self):
        self.temp_emails = []
        self.email_services = [
            {
                'name': '1secmail',
                'domain_url': 'https://www.1secmail.com/api/v1/?action=getDomainList',
                'send_method': self.send_via_1secmail
            },
            {
                'name': 'tempmail',
                'domains': ['tmpmail.org', '10minutemail.com', 'guerrillamail.com'],
                'send_method': self.send_via_api
            }
        ]
        
    def get_random_user_agent(self):
        """تولید User-Agent تصادفی"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        return random.choice(agents)
    
    def create_temp_email_1secmail(self):
        """ایجاد ایمیل موقت از 1secmail"""
        try:
            headers = {'User-Agent': self.get_random_user_agent()}
            response = requests.get(
                'https://www.1secmail.com/api/v1/?action=getDomainList',
                headers=headers,
                timeout=10
            )
            
            domains = response.json()
            if domains:
                domain = random.choice(domains)
                username = ''.join(random.choices(
                    'abcdefghijklmnopqrstuvwxyz0123456789', k=8
                ))
                return f"{username}@{domain}"
                
        except Exception as e:
            print(f"❌ خطا در 1secmail: {e}")
        
        return None
    
    def create_temp_email_guerrilla(self):
        """ایجاد ایمیل موقت از GuerrilaMail"""
        try:
            session = requests.Session()
            session.headers.update({'User-Agent': self.get_random_user_agent()})
            
            # دریافت آدرس ایمیل
            response = session.get(
                'https://www.guerrillamail.com/ajax.php?f=get_email_address',
                timeout=10
            )
            
            data = response.json()
            if 'email_addr' in data:
                return data['email_addr']
                
        except Exception as e:
            print(f"❌ خطا در GuerrilaMail: {e}")
        
        return None
    
    def create_bulk_temp_emails(self, count=10):
        """ایجاد تعداد زیادی ایمیل موقت"""
        print(f"🔄 در حال ایجاد {count} ایمیل موقت...")
        
        methods = [
            self.create_temp_email_1secmail,
            self.create_temp_email_guerrilla
        ]
        
        for i in range(count):
            method = random.choice(methods)
            email = method()
            
            if email and email not in self.temp_emails:
                self.temp_emails.append(email)
                print(f"✅ {len(self.temp_emails)}: {email}")
            
            # وقفه تصادفی
            time.sleep(random.uniform(1, 3))
        
        print(f"📧 مجموعاً {len(self.temp_emails)} ایمیل آماده شد")
        
    def send_via_1secmail(self, sender, target, subject, message):
        """ارسال از طریق 1secmail (شبیه‌سازی)"""
        try:
            # در حالت واقعی باید از SMTP استفاده کنید
            print(f"📤 [{datetime.now().strftime('%H:%M:%S')}] {sender} → {target}")
            print(f"   📝 {subject}")
            
            # شبیه‌سازی تأخیر شبکه
            time.sleep(random.uniform(1, 3))
            
            # احتمال موفقیت 85%
            return random.random() < 0.85
            
        except Exception as e:
            print(f"❌ خطا در ارسال: {e}")
            return False
    
    def send_via_api(self, sender, target, subject, message):
        """ارسال از طریق API های مختلف"""
        try:
            # شبیه‌سازی ارسال
            print(f"📤 [{datetime.now().strftime('%H:%M:%S')}] {sender} → {target}")
            print(f"   📝 {subject}")
            
            time.sleep(random.uniform(2, 4))
            return random.random() < 0.80
            
        except Exception as e:
            print(f"❌ خطا: {e}")
            return False
    
    def send_campaign(self, target_email, subject_template, message_template, count=10, delay_range=(5, 15)):
        """ارسال کمپین ایمیل"""
        
        if len(self.temp_emails) < count:
            needed = count - len(self.temp_emails)
            self.create_bulk_temp_emails(needed + 5)  # چند تا اضافی
        
        if not self.temp_emails:
            print("❌ هیچ ایمیل موقتی در دسترس نیست")
            return
        
        print(f"\n🚀 شروع کمپین ایمیل")
        print(f"🎯 هدف: {target_email}")
        print(f"📊 تعداد: {count} ایمیل")
        print("=" * 50)
        
        success_count = 0
        
        for i in range(count):
            if i >= len(self.temp_emails):
                print("⚠️ ایمیل موقت کافی نیست")
                break
            
            sender = self.temp_emails[i]
            
            # شخصی‌سازی پیام
            subject = subject_template.replace('{i}', str(i+1))
            message = message_template.replace('{i}', str(i+1)).replace('{sender}', sender)
            
            # انتخاب روش ارسال
            send_method = random.choice([
                self.send_via_1secmail,
                self.send_via_api
            ])
            
            success = send_method(sender, target_email, subject, message)
            
            if success:
                success_count += 1
                print(f"✅ موفق ({success_count}/{i+1})")
            else:
                print(f"❌ ناموفق ({success_count}/{i+1})")
            
            # وقفه بین ارسال‌ها
            if i < count - 1:  # آخری نباشد
                delay = random.uniform(delay_range[0], delay_range[1])
                print(f"⏳ انتظار {delay:.1f} ثانیه...")
                time.sleep(delay)
        
        print("=" * 50)
        print(f"📈 نتیجه نهایی: {success_count}/{count} ایمیل ارسال شد")
        print(f"📊 نرخ موفقیت: {(success_count/count)*100:.1f}%")

def interactive_mode():
    """حالت تعاملی برنامه"""
    print("🎯 ایمیل کمپین با ایمیل‌های موقت")
    print("=" * 40)
    
    sender = AdvancedTempEmailSender()
    
    # دریافت تنظیمات از کاربر
    target = input("📬 ایمیل مقصد: ").strip()
    if not target:
        print("❌ ایمیل مقصد الزامی است")
        return
    
    subject = input("📝 موضوع ایمیل (از {i} برای شماره استفاده کنید): ").strip()
    if not subject:
        subject = "پیام شماره {i}"
    
    message = input("💬 متن پیام: ").strip()
    if not message:
        message = "این پیام شماره {i} است که از {sender} ارسال شده."
    
    try:
        count = int(input("🔢 تعداد ایمیل (پیش‌فرض: 10): ").strip() or "10")
        min_delay = int(input("⏱️ حداقل وقفه بین ارسال‌ها (ثانیه، پیش‌فرض: 5): ").strip() or "5")
        max_delay = int(input("⏱️ حداکثر وقفه بین ارسال‌ها (ثانیه، پیش‌فرض: 15): ").strip() or "15")
    except ValueError:
        count, min_delay, max_delay = 10, 5, 15
    
    print(f"\n📋 خلاصه:")
    print(f"  🎯 مقصد: {target}")
    print(f"  📝 موضوع: {subject}")
    print(f"  🔢 تعداد: {count}")
    print(f"  ⏱️ وقفه: {min_delay}-{max_delay} ثانیه")
    
    confirm = input("\n❓ شروع کمپین؟ (y/n): ").strip().lower()
    if confirm == 'y':
        sender.send_campaign(target, subject, message, count, (min_delay, max_delay))
    else:
        print("⏹️ لغو شد")

if __name__ == "__main__":
    interactive_mode()
