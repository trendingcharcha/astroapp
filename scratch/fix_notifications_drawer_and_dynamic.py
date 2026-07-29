import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== FIXING NOTIFICATION DRAWER CLOSE BUTTON & ENHANCING DYNAMIC NOTIFICATIONS ===")

# 1. FIX CLOSE BUTTON 'X' IN NOTIFICATION DRAWER MODAL
target_btn = '<button onclick="toggleNotificationDrawer()" style="background: none; border: none; color: var(--text-muted); font-size: 1.2rem; cursor: pointer; padding: 0 5px;"></button>'
replacement_btn = '<button onclick="toggleNotificationDrawer()" style="background: rgba(232, 200, 121, 0.1); border: 1px solid rgba(232, 200, 121, 0.3); color: var(--gold); font-size: 1.2rem; font-weight: bold; cursor: pointer; padding: 2px 8px; border-radius: 6px; line-height: 1;" title="Close Notifications">✕</button>'

if target_btn in content:
    content = content.replace(target_btn, replacement_btn, 1)
    print("[FIX 1] Added prominent golden 'X' close button to Notification Drawer!")

# 2. ENHANCE DYNAMIC DAY-BY-DAY NOTIFICATIONS BASED ON USER GOAL & KUNDLI
pattern_func = r'function updateSanatanNotifications\(\) \{[\s\S]*?container\.innerHTML = alertsHTML;\s*\}'

replacement_func = """function updateSanatanNotifications() {
      const container = document.getElementById('notification-alerts-list');
      if (!container) return;

      const lang = currentAppLang;
      const isHi = lang === 'hi';
      const dayNum = (typeof selectedRoadmapDay !== 'undefined') ? selectedRoadmapDay : 1;

      // Extract user personal details & Kundli parameters
      const userName = localStorage.getItem('user_name') || localStorage.getItem('kundli_name') || 'Seeker';
      const userGoal = localStorage.getItem('user_goal') || 'job';
      const userProf = localStorage.getItem('user_profession') || 'Professional';
      const lagnaSign = (typeof cachedLagnaSignNum !== 'undefined') ? cachedLagnaSignNum : 0;
      const lagnaLord = signLords[lagnaSign] || 'Sun';
      const lagnaName = signNames[lagnaSign] || 'Aries';
      const lagnaNameHi = signNamesHi[lagnaSign] || 'मेष';

      // Plan Start & Target Date Calculation
      let planStartDate = localStorage.getItem('karma_plan_start_date') || getFormattedDate();
      let startDateObj = new Date(planStartDate);
      if (isNaN(startDateObj.getTime())) startDateObj = new Date();
      let targetDate = new Date(startDateObj.getTime() + (dayNum - 1) * 86400000);

      // Localized Date Header String
      const dateOptions = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' };
      const dateHeaderStr = isHi 
        ? targetDate.toLocaleDateString('hi-IN', dateOptions) 
        : targetDate.toLocaleDateString('en-US', dateOptions);

      // Day of Week Rahu Kaal Map (Rotates dynamically per day!)
      const rahuKaalMap = [
        { en: '04:30 PM - 06:00 PM', hi: 'शाम 04:30 - 06:00', dayEn: 'Sunday', dayHi: 'रविवार' },
        { en: '07:30 AM - 09:00 AM', hi: 'सुबह 07:30 - 09:00', dayEn: 'Monday', dayHi: 'सोमवार' },
        { en: '03:00 PM - 04:30 PM', hi: 'दोपहर 03:00 - 04:30', dayEn: 'Tuesday', dayHi: 'मंगलवार' },
        { en: '12:00 PM - 01:30 PM', hi: 'दोपहर 12:00 - 01:30', dayEn: 'Wednesday', dayHi: 'बुधवार' },
        { en: '01:30 PM - 03:00 PM', hi: 'दोपहर 01:30 - 03:00', dayEn: 'Thursday', dayHi: 'गुरुवार' },
        { en: '10:30 AM - 12:00 PM', hi: 'सुबह 10:30 - 12:00', dayEn: 'Friday', dayHi: 'शुक्रवार' },
        { en: '09:00 AM - 10:30 AM', hi: 'सुबह 09:00 - 10:30', dayEn: 'Saturday', dayHi: 'शनिवार' }
      ];
      const rk = rahuKaalMap[targetDate.getDay()];

      const isEkadashiToday = (dayNum % 15 === 11);
      const isEkadashiTomorrow = (dayNum % 15 === 10);
      const isPradoshToday = (dayNum % 15 === 13);
      const isPurnimaAmavasya = (dayNum % 15 === 0 || dayNum % 15 === 14);
      const daysLeftToEkadashi = (11 - (dayNum % 15) + 15) % 15;

      let alertsHTML = `
        <!-- Live Calendar & Roadmap Day Header -->
        <div style="background: rgba(232, 200, 121, 0.08); border: 1px dashed rgba(232, 200, 121, 0.3); padding: 8px 12px; border-radius: 8px; margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.78rem; font-weight: bold; color: var(--gold);">
            ${dateHeaderStr}
          </span>
          <span style="font-size: 0.7rem; background: var(--gold); color: #0C0922; font-weight: bold; padding: 2px 8px; border-radius: 10px;">
            ${isHi ? `दिन ${dayNum}` : `Day ${dayNum}`}
          </span>
        </div>
      `;

      // 1. DYNAMIC USER GOAL & KUNDLI TRANSIT ALERT (Tailored to Name, Lagna Lord & Goal)
      const goalAlertMapEn = {
        job: `Career Acceleration Notice for ${userName} (${lagnaName} Ascendant): Your ruling planet ${lagnaLord} enhances executive authority today. Schedule high-value work tasks during Abhijit Muhurat.`,
        debt: `Financial Protection Notice for ${userName}: Avoid granting loans or signing debt contracts during Rahu Kaal (${rk.en}).`,
        marriage: `Relationship Harmony Notice for ${userName}: Venus & Moon energy activated for matrimonial progress and peaceful communication.`,
        baby: `Progeny Blessing Notice for ${userName}: Perform Santan Gopal mantra during morning Brahma Muhurat for maximum spiritual energy.`,
        business: `Commercial Expansion Notice for ${userName}: 10th House Lord energy is active. Finalize business proposals outside Rahu Kaal window.`,
        property: `Real Estate Acquisition Notice for ${userName}: Mars energy supported. Inspect property agreements during Abhijit Success Window.`,
        health: `Vitality Spectrum Notice for ${userName}: Drink copper vessel water at sunrise to balance Lagna lord ${lagnaLord} energy.`,
        custom: `Karmic Alignment Notice for ${userName} (${userProf}): Focus on your core goal priorities outside Rahu Kaal.`
      };

      const goalAlertMapHi = {
        job: `${userName} (${lagnaNameHi} लग्न) के लिए करियर त्वरण अलर्ट: आपके स्वामी ग्रह ${signLordsHi[lagnaSign] || lagnaLord} आज अधिकार बढ़ाते हैं। अभिजीत मुहूर्त में महत्वपूर्ण कार्य पूरा करें।`,
        debt: `${userName} के लिए वित्तीय सुरक्षा अलर्ट: राहु काल (${rk.hi}) के दौरान ऋण लेने या वित्तीय समझौतों से बचें।`,
        marriage: `${userName} के लिए वैवाहिक सौहार्द अलर्ट: विवाह प्रस्तावों एवं संवाद हेतु शुक्र व चंद्र ऊर्जा अनुकूल है।`,
        baby: `${userName} के लिए संतान आशीर्वाद अलर्ट: आध्यात्मिक ऊर्जा हेतु ब्रह्म मुहूर्त में संतान गोपाल मंत्र का जाप करें।`,
        business: `${userName} के लिए व्यापार विस्तार अलर्ट: 10वें भाव के स्वामी की ऊर्जा सक्रिय है। राहु काल के बाहर व्यावसायिक निर्णय लें।`,
        property: `${userName} के लिए संपत्ति संचय अलर्ट: मंगल ऊर्जा अनुकूल है। अभिजीत मुहूर्त में संपत्ति दस्तावेजों की समीक्षा करें।`,
        health: `${userName} के लिए स्वास्थ्य ऊर्जा अलर्ट: स्वामी ग्रह ${signLordsHi[lagnaSign] || lagnaLord} की शांति हेतु सूर्योदय पर अर्घ्य दें।`,
        custom: `${userName} (${userProf}) के लिए कर्म संरेखण अलर्ट: राहु काल को छोड़कर अपने प्राथमिक लक्ष्य पर ध्यान दें।`
      };

      alertsHTML += `
        <div style="background: rgba(142, 111, 214, 0.15); border-left: 3px solid var(--purple); padding: 10px 12px; border-radius: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--purple); font-weight: bold; margin-bottom: 4px;">
            <span>${isHi ? 'कुंडली एवं लक्ष्य संरेखण अलर्ट' : 'Kundli & Goal Alignment Notice'}</span>
            <span style="background: var(--purple); color:#fff; padding:1px 6px; border-radius:4px; font-size:0.68rem;">${isHi ? 'व्यक्तिगत' : 'Personalized'}</span>
          </div>
          <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
            ${isHi ? (goalAlertMapHi[userGoal] || goalAlertMapHi.custom) : (goalAlertMapEn[userGoal] || goalAlertMapEn.custom)}
          </p>
        </div>
      `;

      // 2. Ekadashi & Festive Fasting Customization (Day-Wise)
      if (isEkadashiToday) {
        alertsHTML += `
          <div style="background: rgba(232, 200, 121, 0.15); border-left: 3px solid var(--gold); padding: 10px 12px; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--gold); font-weight: bold; margin-bottom: 4px;">
              <span>${isHi ? 'आज पवित्र एकादशी व्रत (11वीं तिथि)' : 'Today Sacred Ekadashi Fast (11th Tithi)'}</span>
              <span style="background: var(--gold); color:#0C0922; padding:1px 6px; border-radius:4px; font-size:0.68rem;">${isHi ? 'आज सक्रिय' : 'Active Today'}</span>
            </div>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
              ${isHi
                ? 'आज एकादशी व्रत है। केवल जल, फल या सात्विक आहार लें। अपने कर्म दोषों को भस्म करने एवं आर्थिक बाधाएं दूर करने हेतु विष्णु सहस्रनाम या स्वामी ग्रह मंत्र का जाप करें।'
                : 'Today is sacred Ekadashi Fast. Consume only water, fruits, or milk. Chant Vishnu Sahasranama & your ruling planet mantra to dissolve financial & karmic blockages.'}
            </p>
          </div>
        `;
      } else if (isEkadashiTomorrow) {
        alertsHTML += `
          <div style="background: rgba(255, 107, 107, 0.12); border-left: 3px solid #ff6b6b; padding: 10px 12px; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #ff6b6b; font-weight: bold; margin-bottom: 4px;">
              <span>${isHi ? '1-दिन पूर्व एकादशी अलर्ट (11:00 AM)' : '1-Day Prior Ekadashi Fast Prep (11:00 AM Alert)'}</span>
              <span style="background: #ff6b6b; color:#fff; padding:1px 6px; border-radius:4px; font-size:0.68rem;">${isHi ? 'कल व्रत' : 'Tomorrow Fast'}</span>
            </div>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
              ${isHi
                ? 'कल पवित्र एकादशी व्रत है। आज सुबह 11:00 बजे से हल्का सात्विक भोजन लें और सूर्यास्त के बाद भारी अन्न से बचें ताकि आपका शरीर और मन कल के व्रत हेतु शुद्ध रहे।'
                : 'Tomorrow is sacred Ekadashi Fast. Starting today at 11:00 AM, consume light sattvic food and avoid heavy grains after sunset to prepare your body & mind.'}
            </p>
          </div>
        `;
      } else if (isPradoshToday) {
        alertsHTML += `
          <div style="background: rgba(142, 68, 173, 0.15); border-left: 3px solid #8e44ad; padding: 10px 12px; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #8e44ad; font-weight: bold; margin-bottom: 4px;">
              <span>${isHi ? 'आज प्रदोष व्रत एवं शिव आराधना' : 'Today Pradosh Vrat & Shiva Sandhya'}</span>
              <span style="background: #8e44ad; color:#fff; padding:1px 6px; border-radius:4px; font-size:0.68rem;">${isHi ? 'आज सक्रिय' : 'Active Today'}</span>
            </div>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
              ${isHi
                ? 'संध्या समय (06:30 PM - 07:30 PM) भगवान शिव के समक्ष शुद्ध घी का दीपक जलाएं और "ॐ नमः शिवाय" का जाप करें।'
                : 'Evening twilight window (06:30 PM - 07:30 PM). Light a pure ghee lamp for Lord Shiva and chant "Om Namah Shivaya" for planetary peace.'}
            </p>
          </div>
        `;
      } else if (isPurnimaAmavasya) {
        alertsHTML += `
          <div style="background: rgba(26, 188, 156, 0.15); border-left: 3px solid #1abc9c; padding: 10px 12px; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #1abc9c; font-weight: bold; margin-bottom: 4px;">
              <span>${isHi ? 'पूर्णिमा / अमावस्या तर्पण एवं दान' : 'Purnima / Amavasya Tarpan & Charity'}</span>
              <span style="background: #1abc9c; color:#fff; padding:1px 6px; border-radius:4px; font-size:0.68rem;">${isHi ? 'आज सक्रिय' : 'Active Today'}</span>
            </div>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
              ${isHi
                ? 'सूर्य देव को जल अर्पित करें, पितरों का ध्यान करें और जरूरतमंदों को सात्विक अन्न दान करें।'
                : 'Offer water to the Sun & Moon, perform ancestral reflection (Pitru Tarpan), and donate food to the needy.'}
            </p>
          </div>
        `;
      } else {
        alertsHTML += `
          <div style="background: rgba(52, 152, 219, 0.12); border-left: 3px solid #3498db; padding: 10px 12px; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #3498db; font-weight: bold; margin-bottom: 4px;">
              <span>${isHi ? `आगामी एकादशी व्रत (${daysLeftToEkadashi} दिन शेष)` : `Upcoming Ekadashi Fast in ${daysLeftToEkadashi} Days`}</span>
              <span style="background: rgba(52, 152, 219, 0.2); color:#3498db; padding:1px 6px; border-radius:4px; font-size:0.68rem;">${isHi ? 'अनुशासन' : 'Discipline'}</span>
            </div>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
              ${isHi
                ? `अगले एकादशी व्रत में ${daysLeftToEkadashi} दिन शेष हैं। सात्विक आहार बनाए रखें और अपने दैनिक कर्म उपाय पूरा करें।`
                : `${daysLeftToEkadashi} days remaining until next Sacred Ekadashi Vrat. Maintain sattvic discipline & daily KarmaQuest remedies.`}
            </p>
          </div>
        `;
      }

      // 3. Day-Specific Rahu Kaal Warning (Rotates daily!)
      alertsHTML += `
        <div style="background: rgba(231, 76, 60, 0.1); border-left: 3px solid #e74c3c; padding: 10px 12px; border-radius: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #e74c3c; font-weight: bold; margin-bottom: 4px;">
            <span>${isHi ? `राहु काल सावधान (${rk.dayHi})` : `Rahu Kaal Alert (${rk.dayEn})`}</span>
            <span>${isHi ? rk.hi : rk.en}</span>
          </div>
          <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
            ${isHi
              ? 'इस अशुभ समय में नए वित्तीय सौदों पर हस्ताक्षर, संपत्ति बुकिंग या शुभ कार्यों की शुरुआत न करें।'
              : 'Inauspicious daily window. Avoid signing major financial contracts, asset purchases, or starting new key tasks during this period.'}
          </p>
        </div>

        <!-- 4. Abhijit Muhurat -->
        <div style="background: rgba(93, 173, 226, 0.1); border-left: 3px solid #5dade2; padding: 10px 12px; border-radius: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #5dade2; font-weight: bold; margin-bottom: 4px;">
            <span>${isHi ? 'अभिजीत मुहूर्त (दैनिक सफलता काल)' : 'Abhijit Muhurat (Daily Success Window)'}</span>
            <span>11:45 AM - 12:30 PM</span>
          </div>
          <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
            ${isHi
              ? 'महत्वपूर्ण बैठकों, अनुबंधों, व्यापारिक निर्णयों और नए कर्म शुरू करने का सबसे शुभ समय।'
              : 'Most auspicious daily window for contracts, major financial decisions, asset bookings & commencing new tasks.'}
          </p>
        </div>

        <!-- 5. Brahma Muhurat -->
        <div style="background: rgba(46, 204, 113, 0.1); border-left: 3px solid #2ecc71; padding: 10px 12px; border-radius: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #2ecc71; font-weight: bold; margin-bottom: 4px;">
            <span>${isHi ? 'ब्रह्म मुहूर्त (साधना काल)' : 'Brahma Muhurat (Spiritual Window)'}</span>
            <span>04:30 AM - 05:15 AM</span>
          </div>
          <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
            ${isHi
              ? 'मंत्र जाप, ध्यान और आत्म-चेतना जगाने के लिए सर्वोत्तम समय।'
              : 'Optimal window for mantra chanting, meditation, and awakening spiritual consciousness.'}
          </p>
        </div>
      `;

      container.innerHTML = alertsHTML;
    }"""

content = re.sub(pattern_func, replacement_func, content, flags=re.MULTILINE)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY ADDED PROMINENT GOLDEN 'X' CLOSE BUTTON AND ENHANCED DYNAMIC NOTIFICATIONS!")
