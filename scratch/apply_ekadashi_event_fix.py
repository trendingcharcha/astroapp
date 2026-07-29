import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'\s*// 5\. EKADASHI FAST & LUNAR FASTING DISCIPLINE[\s\S]*?^\s*\}\s*\n\s*return tasks;'

replacement = """
      // 5. EVENT-ALIGNED VEDIC FASTING & HABIT DISCIPLINE (Only for true events!)
      if (dayNum % 15 === 11) {
        tasks.push({
          category: 'vedic',
          title: isHi ? `पवित्र एकादशी पूर्ण व्रत (11वीं तिथि)` : `Sacred Ekadashi Full Vrat Fast (11th Tithi)`,
          timeWindow: 'Full Day Fast',
          text: isHi
            ? `आज मुख्य एकादशी व्रत है। अन्न का पूर्ण त्याग करें; केवल जल, दूध या ताजे फलों का सेवन करें ताकि आपके कर्म दोष भस्म हों और लक्ष्य सिद्धि प्राप्त हो।`
            : `Observe full Ekadashi Vrat fast today (11th lunar day). Refrain from grains; consume only water, milk, or fruits to burn karmic debt aligned with your goals.`,
          xp: 30,
          color: 'var(--gold)',
          icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E8C879" stroke-width="1.8"><path d="M12 2v2M4.93 4.93l1.41 1.41M20 12h2M17.66 17.66l1.41 1.41M2 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/><circle cx="12" cy="12" r="5" fill="none"/></svg>'
        });
      } else if (dayNum % 15 === 10) {
        tasks.push({
          category: 'vedic',
          title: isHi ? `एकादशी व्रत पूर्व तैयारी (1-दिन पूर्व 11:00 AM अलर्ट)` : `Ekadashi Fast Preparation (1-Day Prior 11:00 AM Alert)`,
          timeWindow: '11:00 AM Alert',
          text: isHi
            ? `कल एकादशी व्रत है। आज सुबह 11:00 बजे से हल्का सात्विक भोजन लें और सूर्यास्त के बाद भारी अन्न से बचें ताकि आपका शरीर और मन कल के व्रत के लिए शुद्ध रहे।`
            : `Tomorrow is sacred Ekadashi Fast. Starting today at 11:00 AM, eat light sattvic food and avoid heavy grains after sunset to prepare your body & mind for tomorrow's fast.`,
          xp: 20,
          color: '#5dade2',
          icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5dade2" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><polygon points="12 6 12 12 16 14"/></svg>'
        });
      } else if (dayNum % 15 === 13) {
        tasks.push({
          category: 'vedic',
          title: isHi ? `प्रदोष व्रत संध्या शिव साधना` : `Pradosh Vrat Evening Shiva Sadhana`,
          timeWindow: '06:30 PM - 07:30 PM',
          text: isHi
            ? `आज प्रदोष व्रत की पावन तिथि है। संध्या समय (06:30 PM - 07:30 PM) भगवान शिव के समक्ष शुद्ध घी का दीपक जलाएं और "ॐ नमः शिवाय" का जाप करें।`
            : `Today is sacred Pradosh Vrat tithi. Light a pure ghee lamp for Lord Shiva in the evening (06:30 PM - 07:30 PM) and chant "Om Namah Shivaya" for planetary peace.`,
          xp: 20,
          color: '#8e44ad',
          icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8e44ad" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><polygon points="12 6 12 12 16 14"/></svg>'
        });
      } else {
        // Daily Planetary Energy Habit aligned with Day of Week & User Goal
        const userName = localStorage.getItem('user_name') || 'Seeker';
        const userProf = localStorage.getItem('user_profession') || 'Professional';
        const dayHabitEn = {
          'Sunday': `Sunday Solar Focus for ${userName}: Offer water to the rising Sun from a copper vessel. Focus on executive leadership for your ${primaryGoal} goal as a ${userProf}.`,
          'Monday': `Monday Moon Alignment for ${userName}: Drink water stored in a silver cup. Practice 10 minutes of silent meditation for emotional balance & relationship clarity.`,
          'Tuesday': `Tuesday Mars Energy for ${userName}: Recite Hanuman Chalisa or "Om Bhaumaya Namah" 11 times to build courage and remove obstacles in your ${primaryGoal} path.`,
          'Wednesday': `Wednesday Mercury Focus for ${userName}: Feed green fodder or vegetables to cows. Focus on strategic communication and analytical work in your ${userProf} tasks.`,
          'Thursday': `Thursday Jupiter Wisdom for ${userName}: Consume a clean sattvic yellow meal with turmeric. Chant "Om Gram Greem Groom Sah Gurave Namah" to expand wealth savings.`,
          'Friday': `Friday Venus Harmony for ${userName}: Wear fresh white or light-colored attire. Maintain pure speech and harmonious relationships to boost abundance.`,
          'Saturday': `Saturday Saturn Discipline for ${userName}: Light a mustard oil lamp under a Peepal tree or donate black sesame seeds to dissolve karmic delays.`
        };

        const dayHabitHi = {
          'Sunday': `${userName} के लिए रविवार सूर्य ध्यान: तांबे के पात्र से उगते सूर्य को अर्घ्य दें। ${userProf} के रूप में अपने लक्ष्य (${primaryGoal}) हेतु नेतृत्व क्षमता मजबूत करें।`,
          'Monday': `${userName} के लिए सोमवार चंद्र संरेखण: चांदी के बर्तन से जल ग्रहण करें। भावनात्मक संतुलन हेतु 10 मिनट मौन ध्यान करें।`,
          'Tuesday': `${userName} के लिए मंगलवार मंगल ऊर्जा: हनुमान चालीसा या "ॐ भौमाय नमः" का 11 बार जाप करें ताकि आपके मार्ग के विघ्न दूर हों।`,
          'Wednesday': `${userName} के लिए बुधवार बुध ध्यान: गायों को हरा चारा खिलाएं। अपने ${userProf} कार्यों में रणनीतिक संचार पर ध्यान केंद्रित करें।`,
          'Thursday': `${userName} के लिए गुरुवार गुरु ज्ञान: हल्दी युक्त सात्विक भोजन ग्रहण करें। "ॐ ग्राम ग्रीं ग्रौं सः गुरवे नमः" का जाप करके धन संचय बढ़ाएं।`,
          'Friday': `${userName} के लिए शुक्रवार शुक्र सौहार्द: स्वच्छ श्वेत या हल्के वस्त्र धारण करें। समृद्धि बढ़ाने हेतु मधुर वाणी व सद्भाव बनाए रखें।`,
          'Saturday': `${userName} के लिए शनिवार शनि अनुशासन: पीपल के नीचे सरसों के तेल का दीपक जलाएं या काले तिल का दान करें ताकि कर्म बाधाएं दूर हों।`
        };

        tasks.push({
          category: 'vedic',
          title: isHi ? `${dayNameHi} दैनिक ग्रह संरेखण एवं सात्विक आदत` : `${dayNameEn} Daily Planetary Alignment & Sattvic Habit`,
          timeWindow: 'Daily Habit Window',
          text: isHi ? (dayHabitHi[dayNameEn] || dayHabitHi['Sunday']) : (dayHabitEn[dayNameEn] || dayHabitEn['Sunday']),
          xp: 15,
          color: '#2ecc71',
          icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2ecc71" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><polygon points="12 6 12 12 16 14"/></svg>'
        });
      }

      return tasks;"""

matches = re.findall(pattern, content, re.MULTILINE)
print(f"Found {len(matches)} match(es)")

if len(matches) == 1:
    content = re.sub(pattern, replacement, content, count=1, flags=re.MULTILINE)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESSFULLY APPLIED FIX!")
else:
    print("MATCH ERROR")
