import os

html_path = r"c:\Users\EARTH\OneDrive\Desktop\Antigravity 2026\Astro AI app\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Define compileMultiGoalMissionData inside generateCoachMission (above compileMissionData)
multi_goal_func = r"""      // Aggregate predictions and remedies for all active goals
      function compileMultiGoalMissionData(lang) {
        const lordDetails = lang === 'hi' ? (vedicMantrasHi[rulingLord] || vedicMantrasHi["Sun"]) : (vedicMantrasEn[rulingLord] || vedicMantrasEn["Sun"]);
        let vListHTML;

        // Vedic Tasks
        if (!hasPartner) {
          const goalVedicContextEn = {
            job: `Perform Surya Namaskaar (12 rounds) before sunrise to activate career and authority vibrations.`,
            debt: `Recite the Shiva Panchakshari mantra "Om Namah Shivaya" 108 times before meals to dissolve financial anxieties.`,
            marriage: `Recite the Katyayani mantra "Om Katyayanyai Namah" 108 times on a Friday morning to attract your destined partner.`,
            baby: `Both partners should recite the Santan Gopal mantra "Om Devaki Sut Govind..." 108 times together each morning.`,
            business: `Perform Ganesh puja on Wednesdays and light incense (dhoop) at your business entrance.`,
            property: `Recite the Bhoomi Sukta prayer (from Atharvaveda) before property visits. Also chant "Om Bhaumaya Namah" 11 times for Mars blessings on property.`,
            health: `Perform Surya Namaskar (sun salutation) at sunrise and drink copper vessel water in the morning for vitality.`,
            custom: `Perform an evening puja with incense and a ghee lamp, focusing your intention on resolving: "${issueText}".`
          };
          const goalVedicContextHi = {
            job: `करियर और अधिकार के स्पंदनों को सक्रिय करने के लिए सूर्योदय से पहले सूर्य नमस्कार (12 चक्र) करें।`,
            debt: `वित्तीय चिंताओं को दूर करने के लिए भोजन से पहले 108 बार शिव पंचाक्षरी मंत्र "ॐ नमः शिवाय" का जाप करें।`,
            marriage: `अपने भाग्यशाली जीवनसाथी को आकर्षित करने के लिए शुक्रवार की सुबह कात्यायनी मंत्र "ॐ कात्यायन्यै नमः" का 108 बार जाप करें।`,
            baby: `संतान सुख के लिए दोनों साथी मिलकर प्रत्येक सुबह 108 बार संतान गोपाल मंत्र "ॐ देवकी सुत गोविंद..." का जाप करें।`,
            business: `बुधवार को गणेश पूजा करें और अपने व्यावसायिक प्रवेश द्वार पर धूप जलाएं।`,
            property: `संपत्ति के दौरों से पहले भूमि सूक्त प्रार्थना (अथर्ववेद से) का पाठ करें। संपत्ति पर मंगल के आशीर्वाद के लिए "ॐ भौमाय नमः" का 11 बार जाप करें।`,
            health: `सूर्योदय के समय सूर्य नमस्कार करें और जीवन शक्ति के लिए सुबह तांबे के बर्तन का पानी पिएं।`,
            custom: `शाम को धूप और घी के दीये के साथ पूजा करें, अपने ध्यान को इस समस्या के समाधान पर केंद्रित करें: "${issueText}"।`
          };

          const contextMap = lang === 'hi' ? goalVedicContextHi : goalVedicContextEn;
          const rituals = [];
          activeGoalsList.forEach(g => {
            let normG = g;
            if (g === 'marriage-single' || g === 'marriage-couple') normG = 'marriage';
            if (g === 'property-single' || g === 'property-couple') normG = 'property';
            const contextKey = ['property-single','property-couple'].includes(g) ? 'property' : ['marriage-single','marriage-couple'].includes(g) ? 'marriage' : (normG in contextMap ? normG : 'custom');
            const ritual = contextMap[contextKey] || contextMap.custom;
            const label = (lang === 'hi' ? (goalLabelsHi[g] || goalLabelsEn[g] || g) : (goalLabelsEn[g] || g));
            rituals.push(`<strong>${label}:</strong> ${ritual}`);
          });
          const ritualsHTML = rituals.map(r => `<div style="margin-top: 4px; padding-left: 10px; border-left: 2px solid var(--gold);">${r}</div>`).join('');

          if (lang === 'hi') {
            vListHTML = `
              <li style="margin-bottom: 10px;"><strong>शासक ग्रह मंत्र:</strong> प्रत्येक सुबह पूर्व की ओर मुंह करके 108 बार <strong>"${lordDetails.mantra}"</strong> का लगातार 40 दिनों तक जाप करें।</li>
              <li style="margin-bottom: 10px;"><strong>पवित्र पाठ:</strong> ${lordDetails.text}</li>
              <li style="margin-bottom: 10px;"><strong>लक्ष्य अनुष्ठान:</strong> ${ritualsHTML}</li>
              <li><strong>एकादशी व्रत:</strong> अपने लक्ष्यों से जुड़े कर्मों को संरेखित करने के लिए प्रति माह कम से कम एक एकादशी का व्रत रखें, जिसमें केवल फल या पानी का सेवन करें।</li>
            `;
          } else {
            vListHTML = `
              <li style="margin-bottom: 10px;"><strong>Ruling Planet Mantra:</strong> Chant <strong>"${lordDetails.mantra}"</strong> exactly 108 times each morning facing East for 40 consecutive days.</li>
              <li style="margin-bottom: 10px;"><strong>Sacred Text:</strong> ${lordDetails.text}</li>
              <li style="margin-bottom: 10px;"><strong>Goal Ritual(s):</strong> ${ritualsHTML}</li>
              <li><strong>Ekadashi Fast:</strong> Observe at least one Ekadashi (11th lunar day) fast per month, drinking only fruit or water, to burn karmic debt aligned with your goals.</li>
            `;
          }
        } else {
          const partnerLordDetails = lang === 'hi' ? (vedicMantrasHi[partnerRulingLord] || vedicMantrasHi["Sun"]) : (vedicMantrasEn[partnerRulingLord] || vedicMantrasEn["Sun"]);
          const coupleGoalRitualsEn = {
            marriage: `Both partners should recite the Vivah Sukta verses from the Rigveda together each morning and offer flowers to Lord Vishnu on Thursdays.`,
            baby: `Both partners should recite the Santan Gopal mantra "Om Devaki Sut Govind..." 108 times together each morning.`,
            property: `Both partners should offer water, a flower, and a pinch of turmeric to a rising sun, and chant "Om Bhaumaya Namah" 11 times together before any property visits.`,
            debt: `Both partners should recite the Shiva Panchakshari mantra together 108 times on Monday mornings while holding water in cupped hands.`,
            custom: `Both partners should perform evening puja together with ghee lamp, flowers, and focused collective intention on resolving the shared challenge.`
          };
          const coupleGoalRitualsHi = {
            marriage: `दोनों साथी प्रत्येक सुबह मिलकर ऋग्वेद के विवाह सूक्त श्लोकों का पाठ करें और गुरुवार को भगवान विष्णु को फूल अर्पित करें।`,
            baby: `दोनों साथी प्रत्येक सुबह मिलकर संतान गोपाल मंत्र "ॐ देवकी सुत गोविंद..." का 108 बार जाप करें।`,
            property: `दोनों साथी किसी भी संपत्ति के दौरे से पहले उगते सूर्य को जल, फूल और एक चुटकी हल्दी अर्पित करें, और मिलकर 11 बार "ॐ भौमाय नमः" का जाप करें।`,
            debt: `दोनों साथी सोमवार की सुबह हाथों में जल लेकर मिलकर 108 बार शिव पंचाक्षरी मंत्र का जाप करें।`,
            custom: `दोनों साथी शाम को मिलकर घी के दीपक, फूलों और सामूहिक ध्यान के साथ साझा चुनौती को हल करने के लिए पूजा करें।`
          };

          const coupleMap = lang === 'hi' ? coupleGoalRitualsHi : coupleGoalRitualsEn;
          const coupleRituals = [];
          activeGoalsList.forEach(g => {
            let normG = g;
            if (g === 'marriage-single' || g === 'marriage-couple') normG = 'marriage';
            if (g === 'property-single' || g === 'property-couple') normG = 'property';
            const coupleContextKey = normG in coupleMap ? normG : 'custom';
            const ritual = coupleMap[coupleContextKey];
            const label = (lang === 'hi' ? (goalLabelsHi[g] || goalLabelsEn[g] || g) : (goalLabelsEn[g] || g));
            coupleRituals.push(`<strong>${label}:</strong> ${ritual}`);
          });
          const coupleRitualsHTML = coupleRituals.map(r => `<div style="margin-top: 4px; padding-left: 10px; border-left: 2px solid var(--gold);">${r}</div>`).join('');

          if (lang === 'hi') {
            vListHTML = `
              <li style="margin-bottom: 10px;"><strong>${name} का मंत्र:</strong> प्रत्येक सुबह 108 बार <strong>"${lordDetails.mantra}"</strong> का जाप करें (आपके लग्न के स्वामी: ${rulingLord})।</li>
              <li style="margin-bottom: 10px;"><strong>${partnerName || 'साथी'} का मंत्र:</strong> प्रत्येक सुबह 108 बार <strong>"${partnerLordDetails.mantra}"</strong> का जाप करें (उनके लग्न के स्वामी: ${partnerRulingLord})।</li>
              <li style="margin-bottom: 10px;"><strong>युगल लक्ष्य अनुष्ठान:</strong> ${coupleRitualsHTML}</li>
              <li style="margin-bottom: 10px;"><strong>साझा पवित्र पाठ:</strong> अपने साझा लक्ष्यों के लिए ईश्वरीय सहायता प्राप्त करने के लिए प्रत्येक शाम एक साथ गुरु स्तोत्र या शिव पुराण का पाठ करें।</li>
              <li><strong>एकादशी व्रत:</strong> सामूहिक कर्म ऊर्जा को संरेखित करने के लिए इस महीने कम से कम एक बार दोनों मिलकर एकादशी व्रत का पालन करें।</li>
            `;
          } else {
            vListHTML = `
              <li style="margin-bottom: 10px;"><strong>${name}'s Mantra:</strong> Chant <strong>"${lordDetails.mantra}"</strong> 108 times each morning (ruler of your Lagna: ${rulingLord}).</li>
              <li style="margin-bottom: 10px;"><strong>${partnerName || 'Partner'}'s Mantra:</strong> Chant <strong>"${partnerLordDetails.mantra}"</strong> 108 times each morning (ruler of their Lagna: ${partnerRulingLord}).</li>
              <li style="margin-bottom: 10px;"><strong>Couple Goal Ritual(s):</strong> ${coupleRitualsHTML}</li>
              <li style="margin-bottom: 10px;"><strong>Shared Sacred Text:</strong> Read the Guru Stotra or Shiva Purana together each evening to invite divine support for your shared goals.</li>
              <li><strong>Ekadashi Fast:</strong> Both observe Ekadashi fast together at least once this month to align collective karmic energies.</li>
            `;
          }
        }

        // Lal Kitab Remedies
        const remMap = lang === 'hi' ? lalkitabRemediesHi : lalkitabRemediesEn;
        let allRemedies = [];
        const itemsPerGoal = activeGoalsList.length === 1 ? 6 : (activeGoalsList.length === 2 ? 3 : 2);

        activeGoalsList.forEach(g => {
          let rKey = g;
          if (g === 'marriage-single' || g === 'marriage-couple') rKey = 'marriage';
          if (g === 'property-single' || g === 'property-couple') rKey = 'property';
          if (g === 'custom') rKey = "custom_" + customCategory;
          
          let goalRemedies = remMap[rKey] || remMap["job"];
          if (goalRemedies) {
            let customized = [...goalRemedies];
            if (hasPartner) {
              let normG = g;
              if (g === 'marriage-single' || g === 'marriage-couple') normG = 'marriage';
              if (g === 'property-single' || g === 'property-couple') normG = 'property';
              
              if (lang === 'hi') {
                if (normG === 'baby' || customCategory === 'pregnancy') {
                  customized[1] = `संतान आशीर्वाद को मजबूत करने के लिए आप और ${partnerName || 'आपके साथी'} दोनों को मिलकर बरगद के पेड़ की जड़ में दूध या मीठा पानी चढ़ाना चाहिए और माथे पर गीली मिट्टी का तिलक लगाना चाहिए।`;
                } else if (normG === 'property' || customCategory === 'property') {
                  customized[1] = `सामूहिक मंगल/भूमि ऊर्जा का आह्वान करने के लिए आप और ${partnerName || 'आपके साथी'} दोनों को मिलकर उगते सूर्य को एक चम्मच शहद मिला हुआ जल अर्पित करना चाहिए।`;
                } else if (normG === 'marriage') {
                  customized[1] = `सामंजस्यपूर्ण विवाह तरंगों के लिए आप और ${partnerName || 'आपके साथी'} दोनों को मिलकर गुरुवार की शाम विष्णु मंदिर में घी का दीपक जलाना चाहिए।`;
                } else {
                  customized[1] = `शुक्र/चंद्र अनुकूलता को मजबूत करने के लिए आप और ${partnerName || 'आपके साथी'} दोनों को मिलकर सोमवार की सुबह सफेद गाय को भोजन कराना चाहिए या चावल और दूध का दान करना चाहिए।`;
                }
              } else {
                if (normG === 'baby' || customCategory === 'pregnancy') {
                  customized[1] = `Both you and ${partnerName || 'your partner'} should offer milk or sweet water to a banyan tree root together and apply the wet soil tilak on your foreheads to strengthen progeny blessings.`;
                } else if (normG === 'property' || customCategory === 'property') {
                  customized[1] = `Both you and ${partnerName || 'your partner'} should offer fresh water mixed with a small spoon of honey to the rising Sun together to invoke collective Mars/land energy.`;
                } else if (normG === 'marriage') {
                  customized[1] = `Both you and ${partnerName || 'your partner'} should light a ghee lamp at a Vishnu temple together on Thursday evenings for harmonious marital vibrations.`;
                } else {
                  customized[1] = `Both you and ${partnerName || 'your partner'} should feed a white cow or donate rice and milk on Monday mornings to strengthen Venus/Moon compatibilities.`;
                }
              }
            }
            
            const sliced = customized.slice(0, itemsPerGoal);
            sliced.forEach(rem => {
              if (!allRemedies.includes(rem)) {
                allRemedies.push(rem);
              }
            });
          }
        });

        if (allRemedies.length === 0) {
          allRemedies = [...(remMap["job"] || [])];
        }

        const lListHTML = allRemedies.slice(0, 8).map((r, i) =>
          `<li style="margin-bottom: 10px;"><strong>${lang === 'hi' ? 'उपाय' : 'Remedy'} ${i+1}:</strong> ${r}</li>`
        ).join('');

        // Vastu Suggestions
        const vastuMap = lang === 'hi' ? vastuSuggestionsHi : vastuSuggestionsEn;
        const vastuDirectives = [];

        activeGoalsList.forEach(g => {
          let normG = g;
          if (g === 'marriage-single' || g === 'marriage-couple') normG = 'marriage';
          if (g === 'property-single' || g === 'property-couple') normG = 'property';
          
          let vastuGoal = normG;
          if (normG === 'custom') {
            vastuGoal = "custom_" + customCategory;
          }
          
          let vastuText = vastuMap[vastuGoal] || vastuMap["job"];
          if (normG === 'baby' && hasPartner) {
            if (lang === 'hi') {
              if (babyNum === "1") {
                vastuText = `सुनिश्चित करें कि आपका साझा बिस्तर दक्षिण-पश्चिम दिशा में रखा गया है। अपने बेडरूम में गहरे रंगों का उपयोग करने से बचें; गर्भावस्था के अनुकूल तरंगों के लिए हल्के क्रीम, गुलाबी या हल्के पीले रंगों को प्राथमिकता दें। उत्तर-पूर्व कोने को साफ रखें।`;
              } else if (babyNum === "2") {
                vastuText = `सुनिश्चित करें कि आपके घर का उत्तर-पूर्व क्षेत्र साफ है। शांत वातावरण बनाए रखने के लिए अपने पहले बच्चे के खिलौनों को अपने सोने के बेडरूम से दूर रखें। बेडरूम के पूर्व क्षेत्र में ताजे सफेद फूल रखें।`;
              } else if (babyNum === "3") {
                vastuText = `घर में बढ़ती हुई संतान ऊर्जा को आमंत्रित करने के लिए अपने रहने वाले क्षेत्र के पूर्वी हिस्से में एक स्वस्थ हरा पौधा या पारिवारिक चित्र लगाएं। बच्चों के कमरे में पूर्व या उत्तर की ओर खिड़कियां रखें।`;
              }
            } else {
              if (babyNum === "1") {
                vastuText = `Ensure your shared bed is placed in the South-West direction. Avoid using aggressive colors (like red or dark blue) in your bedroom; prefer warm cream, pastel pink, or light yellow tones to support pregnancy vibrations. Keep North-East zone clean and fresh.`;
              } else if (babyNum === "2") {
                vastuText = `Ensure the North-East zone of your home is clean. Keep your first child's toys away from your bedroom to maintain tranquil pregnancy vibes. Place fresh white flowers in the East zone of your bedroom.`;
              } else if (babyNum === "3") {
                vastuText = `Place a healthy green plant or a family portrait in the East zone of your shared living space to invite growing domestic progeny energies. Ensure the children's room has East or North-facing windows.`;
              }
            }
          } else if (normG === 'property' && hasPartner) {
            if (lang === 'hi') {
              vastuText = `आप दोनों को संभावित ${propertyType} पर एक साथ जाना चाहिए और मूल्यांकन करना चाहिए: मुख्य द्वार की दिशा (पूर्व/उत्तर को प्राथमिकता दें), उत्तर-पूर्व क्षेत्र (खुला/हल्का होना चाहिए), रसोई (दक्षिण-पूर्व में होनी चाहिए)। उत्तर-पूर्व में शौचालय या बैठने/सोने के क्षेत्र के ऊपर कंक्रीट बीम वाली संपत्तियों से बचें।`;
            } else {
              vastuText = `Both of you should visit the prospective ${propertyType} together and assess: main door direction (prefer East/North), North-East zone (should be open/light), kitchen (should be in South-East). Avoid properties with toilets in North-East or beams over the main sitting/sleeping area.`;
            }
          } else if (normG === 'marriage' && hasPartner) {
            if (lang === 'hi') {
              vastuText = `सुनिश्चित करें कि आपके बेडरूम का दक्षिण-पश्चिम (संबंध क्षेत्र) साफ है, वहां रोज़ क्वार्ट्ज क्रिस्टल का गोला है, और बिस्तर को सीधे प्रतिबिंबित करने वाले कोई दर्पण नहीं हैं। टूटे सजावटी सामान हटा दें।`;
            } else {
              vastuText = `Ensure the South-West (relationship zone) of your shared bedroom is clean, has a rose quartz sphere, and contains no mirrors directly reflecting the bed. Remove any broken decor items.`;
            }
          } else if (hasPartner && customCategory === "pregnancy") {
            if (lang === 'hi') {
              vastuText = `सुनिश्चित करें कि आपका साझा बिस्तर दक्षिण-पश्चिम दिशा में रखा गया है। अपने बेडरूम में गहरे रंगों का उपयोग करने से बचें; हल्के क्रीम, गुलाबी या हल्के पीले रंगों को प्राथमिकता दें।`;
            } else {
              vastuText = `Ensure your shared bed is placed in the South-West direction. Avoid using aggressive colors in your bedroom; prefer warm cream, pastel pink, or light yellow tones.`;
            }
          }

          const label = (lang === 'hi' ? (goalLabelsHi[g] || goalLabelsEn[g] || g) : (goalLabelsEn[g] || g));
          vastuDirectives.push(`<strong>${label}:</strong> ${vastuText}`);
        });

        const vastuDirectivesHTML = vastuDirectives.map(d => `<div style="margin-top: 4px; padding-left: 10px; border-left: 2px solid var(--gold);">${d}</div>`).join('');

        const vVastuHTML = `
          <li style="margin-bottom: 10px;"><strong>${lang === 'hi' ? 'वास्तु निर्देश' : 'Vastu Directive(s)'}:</strong> ${vastuDirectivesHTML}</li>
          <li><strong>${lang === 'hi' ? 'दैनिक दिशा संरेखण' : 'Daily Direction Alignment'}:</strong> ${lang === 'hi' ? 'सकारात्मक ऊर्जा प्रवाह के लिए काम करते या ध्यान लगाते समय पूर्व या उत्तर दिशा की ओर मुख करें।' : 'Face East or North while working or meditating to align with positive energetic currents.'}</li>
        `;

        // Practical Tasks
        const practicalMap = lang === 'hi' ? practicalActionsHi : practicalActions;
        let allActions = [];
        const actionsPerGoal = activeGoalsList.length === 1 ? 4 : 2;

        activeGoalsList.forEach(g => {
          let normG = g;
          if (g === 'marriage-single' || g === 'marriage-couple') normG = 'marriage';
          if (g === 'property-single' || g === 'property-couple') normG = 'property';
          
          let actionsGoal = normG;
          if (normG === 'custom') {
            actionsGoal = "custom_" + customCategory;
          }
          
          let goalActions = [...(practicalMap[actionsGoal] || practicalMap["job"])];
          goalActions = goalActions.filter(a => a !== undefined);

          if (g === 'baby') {
            if (hasPartner) {
              if (lang === 'hi') {
                if (babyNum === "1") {
                  goalActions = [
                    `स्वयं: एक स्वस्थ प्रसवपूर्व आहार बनाए रखें और आज ही अपने दैनिक विटामिन सेवन को दर्ज करें।`,
                    `साथी (${partnerName}): अपने जीवनसाथी के लिए शारीरिक तनाव को कम करने के लिए household tasks में सहायता करें।`,
                    `संयुक्त कदम: रिश्ते की ऊर्जा को संरेखित करने के लिए आप और ${partnerName} दोनों मिलकर 15 मिनट ध्यान करें।`,
                    `संयुक्त योजना: इस महीने दौरा करने के लिए 3 local health clinics या मातृत्व केंद्रों को शॉर्टलिस्ट करें।`
                  ];
                } else if (babyNum === "2") {
                  goalActions = [
                    `स्वयं: health metrics और post-pregnancy recovery के संकेतों को ट्रैक करने के लिए 15 मिनट लें।`,
                    `साथी (${partnerName}): अपने पहले बच्चे (उम्र: ${firstBabyAge} वर्ष) की देखभाल में 30 मिनट का समय बिताएं।`,
                    `संयुक्त कदम: ${partnerName} के साथ चर्चा करें कि पहले बच्चे को नए भाई या बहन के आगमन के लिए मानसिक रूप से कैसे तैयार किया जाए।`,
                    `संयुक्त योजना: निरीक्षण करें कि पहले बच्चे के कौन से सामान दोबारा काम आ सकते।`
                  ];
                } else if (babyNum === "3") {
                  goalActions = [
                    `स्वयं: आराम करने, हल्के खिंचाव का अभ्यास करने और आज पोषण मेट्रिक्स लॉग करने के लिए 20 मिनट लें।`,
                    `साथी (${partnerName}): आज अपने पहले दो बच्चों (उम्र: ${firstBabyAge} और ${secondBabyAge}) की दैनिक दिनचर्या और पढ़ाई की जिम्मेदारी संभालें।`,
                    `संयुक्त कदम: पांच सदस्यों के परिवार के लिए आवश्यक वित्तीय समायोजन का खाका तैयार करने के लिए ${partnerName} के साथ 20 मिनट बैठें।`,
                    `संयुक्त योजना: तीन बच्चों को समायोजित करने के लिए शयनकक्ष के पुनर्गठन या अंतरिक्ष वितरण पर चर्चा करें।`
                  ];
                }
              } else {
                if (lang === 'hi') {
                  if (babyNum === "1") {
                    goalActions = [
                      `आज प्रसवपूर्व स्वास्थ्य, फोलिक एसिड और आयरन से भरपूर एक पौष्टिक मेनू की योजना बनाएं।`,
                      `अपने स्थानीय शहर क्षेत्र में उच्च श्रेणी के स्त्री रोग विशेषज्ञों या मातृत्व विशेषज्ञों की सूची बनाएं।`,
                      `तनाव के स्तर को कम करने के लिए हल्के श्वास व्यायाम (प्राणायाम) करने में 20 मिनट का समय बिताएं।`,
                      `प्रजनन काल और स्वास्थ्य संकेतकों को ट्रैक करने के लिए दैनिक स्वास्थ्य कैलेंडर बनाए रखें।`
                    ];
                  } else if (babyNum === "2") {
                    goalActions = [
                      `पहली गर्भावस्था के बाद से स्वास्थ्य संकेतकों की समीक्षा के लिए बाल रोग विशेषज्ञ से परामर्श करें (पहला बच्चा ${firstBabyAge} वर्ष का है)।`,
                      `पहले बच्चे के पुनः उपयोग किए जा सकने वाले शिशु सामानों की एक चेकलिस्ट बनाएं।`,
                      `कई बच्चों के पालन-पोषण और समय प्रबंधन के तरीकों को पढ़ने के लिए 20 मिनट का समय दें।`,
                      `प्रसवपूर्व स्वास्थ्य मार्करों का आकलन करने के लिए एक नियमित स्वास्थ्य जांच का समय निर्धारित करें।`
                    ];
                  } else if (babyNum === "3") {
                    goalActions = [
                      `तीन बच्चों (मौजूदा उम्र: ${firstBabyAge} और ${secondBabyAge}) के खर्चों की व्यवस्था के लिए अपनी पारिवारिक बजट बहीखाते की समीक्षा करें।`,
                      `सभी तीन बच्चों के लिए कमरों या जगह के वितरण पर चर्चा करने के लिए 30 मिनट का समय निकालें।`,
                      `एक बड़े परिवार के लिए मानसिक सहनशक्ति विकसित करने के लिए 15 मिनट का ध्यान सत्र करें।`,
                      `मातृ स्वास्थ्य संकेतकों की समीक्षा के लिए एक प्राथमिक स्वास्थ्य परामर्श शेड्यूल करें।`
                    ];
                  }
                } else {
                  if (babyNum === "1") {
                    goalActions = [
                      `Plan a nutritious prenatal menu rich in folate, iron, and greens today.`,
                      `Research and list high-rated gynecologists or birthing specialists in your city area.`,
                      `Spend 20 minutes practicing deep breathing exercises (Pranayama) to stabilize cortisol levels.`,
                      `Maintain a daily fertility and health tracking log to monitor cycles and wellness markers.`
                    ];
                  } else if (babyNum === "2") {
                    goalActions = [
                      `Consult with a pediatrician or doctor to review health markers since your first pregnancy (first child is ${firstBabyAge} years old).`,
                      `Create a checklist of baby essentials and gear you can reuse from your first child.`,
                      `Dedicate 20 minutes to read about managing parenting schedules and routines with multiple children.`,
                      `Schedule a routine health check-up to assess prenatal compatibility and health markers.`
                    ];
                  } else if (babyNum === "3") {
                    goalActions = [
                      `Review your monthly family budget ledger to account for the expenses of raising three children (existing ages: ${firstBabyAge} & ${secondBabyAge}).`,
                      `Set aside 30 minutes to discuss space/room distribution for all three children.`,
                      `Practice a 15-minute mindfulness session to cultivate mental resilience for a larger family.`,
                      `Schedule a primary healthcare consultation to review maternal health pointers.`
                    ];
                  }
                }
              }
            } else if (hasPartner) {
              if (lang === 'hi') {
                if (customCategory === "pregnancy") {
                  goalActions = [
                    `स्वयं (महिला साथी): अपने शारीरिक स्वास्थ्य संकेतकों को ट्रैक करें, गर्भावस्था डायरी बनाए रखें, और विटामिन लें।`,
                    `साथी (${partnerName}): साथी की शारीरिक थकान को कम करने के लिए एक भारी घरेलू काम खुद संभालें।`,
                    `संयुक्त कदम: तनाव के स्तर को संतुलित करने के लिए शाम को मिलकर 15 मिनट श्वास व्यायाम (अनुलोम विलोम) करें।`,
                    `संयुक्त योजना: उन प्रश्नों की एक साझा सूची तैयार करें जिन्हें आप अगले सप्ताह की जांच के दौरान डॉक्टर से पूछना चाहते हैं।`
                  ];
                } else if (customCategory === "property") {
                  goalActions = [
                    `स्वयं: अपने बजट से मेल खाने वाली संपत्तियों के लिए ऑनलाइन लिस्टिंग खोजें और 3 विकल्पों को शॉर्टलिस्ट करें।`,
                    `साथी (${partnerName}): वित्तीय बजट, बचत या गृह ऋण प्रलेखन विकल्पों की समीक्षा करने में 15 मिनट का समय दें।`,
                    `संयुक्त कदम: शॉर्टलिस्ट किए गए विकल्पों को एक साथ देखने में 20 मिनट का समय बिताएं और स्थान प्राथमिकताओं को संरेखित करें।`,
                    `संयुक्त योजना: इस सप्ताहांत एक साथ भौतिक संपत्ति का निरीक्षण करने के लिए एक संयुक्त साइट विजिट शेड्यूल करें।`
                  ];
                } else {
                  goalActions = [
                    `स्वयं: आज 15 मिनट का समय निकालकर एक संबंध चिंता या लक्ष्य लिखें जिसे आप ${partnerName} के साथ साझा करना चाहते हैं।`,
                    `साथी (${partnerName}): उनसे कहें कि सक्रिय रूप से सुनने में 15 मिनट बिताएं बिना कोई अवांछित सलाह दिए।`,
                    `संयुक्त कदम: आप और ${partnerName} दोनों मिलकर 20 मिनट बाहर टहलें या साझा योजना पर चर्चा करते हुए चाय साझा करें।`,
                    `ऊर्जावान संरेखण: साथी के ग्रहों के स्पंदनों को सामंजस्य में लाने के लिए आज मनभावन हल्के रंग (जैसे क्रीम या पीला) पहनें।`
                  ];
                }
              } else {
                if (customCategory === "pregnancy") {
                  goalActions = [
                    `Self (Female Partner): Track your physical health indicators, keep a pregnancy diary, and take prenatal vitamins.`,
                    `Partner (${partnerName}): Take over one heavy household chore (like carrying groceries or deep cleaning) to minimize physical fatigue for your partner.`,
                    `Joint Action: Spend 15 minutes in the evening doing light breathing exercises (Anulom Vilom) together to harmonize stress levels.`,
                    `Joint Planning: Draft a shared list of questions you want to ask your gynecologist or consultant during next week's check-up.`
                  ];
                } else if (customCategory === "property") {
                  goalActions = [
                    `Self: Spend 15 minutes searching online listings for properties matching your target criteria and shortlist 3 choices.`,
                    `Partner (${partnerName}): Spend 15 minutes reviewing the financial budget, savings, or loan documentation options.`,
                    `Joint Action: Spend 20 minutes looking at the shortlisted options together and align on your location priorities.`,
                    `Joint Action: Schedule a joint site visit or broker call to inspect a physical property together this weekend.`
                  ];
                } else {
                  goalActions = [
                    `Self: Take 15 minutes today to write down a relationship concern or goal you want to discuss with ${partnerName}.`,
                    `Partner (${partnerName}): Ask them to spend 15 minutes listening actively to your daily experiences without offering unsolicited advice.`,
                    `Joint Action: Both you and ${partnerName} should spend 20 minutes walking together outdoors or sharing a relaxing tea while discussing a shared domestic plan.`,
                    `Energetic Sync: Wear pleasing light colors today (like cream, pastel pink, or light yellow) to harmonize both partners' planetary vibrations.`
                  ];
                }
              }
            }

            const sliced = goalActions.slice(0, actionsPerGoal);
            sliced.forEach(act => {
              if (!allActions.includes(act)) {
                allActions.push(act);
              }
            });
          });

        if (allActions.length === 0) {
          allActions = [...(practicalMap["job"] || [])];
        }

        const pListHTML = allActions.slice(0, 6).map((a, i) =>
          `<li><strong>${lang === 'hi' ? 'कदम' : 'Action Step'} ${i+1}:</strong> ${a}</li>`
        ).join('');

        // Astro predictions text
        let predictionHTML;
        if (lang === 'hi') {
          predictionHTML = `
            <p style="margin: 0 0 10px 0;"><strong>ज्योतिषीय लग्न (Lagna):</strong> <span style="color: var(--gold);">${lagnaNameHi} (${lagnaName})</span> | <strong>शासक ग्रह:</strong> <span style="color: #5dade2;">${rulingLord}</span></p>
            <p style="margin: 0 0 10px 0;">आपकी कुंडली बताती है कि आपके लग्न स्वामी <strong>${rulingLord}</strong> वर्तमान में आपके 90-दिवसीय कर्म चक्र की ओर मजबूत ऊर्जा किरणें संचारित कर रहे हैं। समर्पित अनुशासन के साथ, आपका व्यक्तिगत ऊर्जा संरेखण आगामी 90 दिनों में चरम प्रकटीकरण शक्ति तक पहुंच जाएगा।</p>
            <div style="background: rgba(232, 200, 121, 0.06); padding: 12px; border-radius: 8px; border-left: 3px solid var(--gold); margin-top: 10px;">
              <strong style="color: var(--gold); display: block; margin-bottom: 4px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle; margin-right:4px;"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> सक्रिय लक्ष्यों का ज्योतिषीय पूर्वानुमान:</strong>
              <ul style="margin: 4px 0 0 18px; padding: 0;">
                ${activeGoalsList.map(g => {
                  const gLabel = goalLabelsHi[g] || goalLabelsEn[g] || g;
                  return `<li style="margin-bottom: 4px;"><strong>${gLabel}:</strong> ${rulingLord} के स्थान के तहत अत्यधिक अनुकूल ग्रह समर्थन पाया गया। त्वरित सफलता के लिए नीचे दिए गए उपायों का पालन करें।</li>`;
                }).join('')}
              </ul>
            </div>
          `;
        } else {
          predictionHTML = `
            <p style="margin: 0 0 10px 0;"><strong>Astrological Ascendant (Lagna):</strong> <span style="color: var(--gold);">${lagnaName} (${lagnaNameHi})</span> | <strong>Ruling Planet:</strong> <span style="color: #5dade2;">${rulingLord}</span></p>
            <p style="margin: 0 0 10px 0;">Your horoscope indicates that your Lagna Lord <strong>${rulingLord}</strong> is currently transmitting strong activating rays towards your 90-day karmic cycle. With dedicated discipline, your personal energy alignment will reach peak manifestation power over the upcoming 90 days.</p>
            <div style="background: rgba(232, 200, 121, 0.06); padding: 12px; border-radius: 8px; border-left: 3px solid var(--gold); margin-top: 10px;">
              <strong style="color: var(--gold); display: block; margin-bottom: 4px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle; margin-right:4px;"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> Active Goals Astrological Forecast:</strong>
              <ul style="margin: 4px 0 0 18px; padding: 0;">
                ${activeGoalsList.map(g => {
                  const gLabel = goalLabelsEn[g] || g;
                  return `<li style="margin-bottom: 4px;"><strong>${gLabel}:</strong> Highly favorable planetary support detected under ${rulingLord}'s placement. Follow the remedies below for accelerated success.</li>`;
                }).join('')}
              </ul>
            </div>
          `;
        }

        // Mission Type
        const goalTitleMapEn = {
          'job': 'Career Mission',
          'debt': 'Wealth Clearing Mission',
          'marriage': 'Marriage Prediction Mission',
          'baby': 'Baby Planning Mission',
          'business': 'Business Growth Mission',
          'property': 'Dream Home Mission',
          'health': 'Health & Healing Mission',
          'custom': 'Life Resolution Mission'
        };
        const goalTitleMapHi = {
          'job': 'करियर मिशन',
          'debt': 'धन शुद्धि मिशन',
          'marriage': 'विवाह भविष्यवाणी मिशन',
          'baby': 'संतान योजना मिशन',
          'business': 'व्यापार विकास मिशन',
          'property': 'सपनों का घर मिशन',
          'health': 'स्वास्थ्य और उपचार मिशन',
          'custom': 'जीवन समाधान मिशन'
        };

        const missionTypes = [];
        activeGoalsList.forEach(g => {
          let normG = g;
          if (g === 'marriage-single' || g === 'marriage-couple') normG = 'marriage';
          if (g === 'property-single' || g === 'property-couple') normG = 'property';
          const type = lang === 'hi' ? (goalTitleMapHi[normG] || 'दैनिक एस्ट्रो मिशन') : (goalTitleMapEn[normG] || 'Daily Astro Mission');
          if (!missionTypes.includes(type)) {
            missionTypes.push(type);
          }
        });
        const combinedMissionType = missionTypes.join(' & ');

        let titleText = hasPartner
          ? (lang === 'hi' ? `${name} और ${partnerName || 'साथी'} का ${combinedMissionType}` : `${name} & ${partnerName || 'Partner'}'s ${combinedMissionType}`)
          : (lang === 'hi' ? `${name} का ${combinedMissionType}` : `${name}'s ${combinedMissionType}`);

        return {
          vListHTML,
          lListHTML,
          vVastuHTML,
          pListHTML,
          predictionHTML,
          titleText
        };
      }
"""

# Replace the calls
old_calls = """      // Compile both languages!
      const missionEn = compileMissionData('en');
      const missionHi = compileMissionData('hi');"""

new_calls = """      // Compile both languages using multi-goal aggregator!
      const missionEn = compileMultiGoalMissionData('en');
      const missionHi = compileMultiGoalMissionData('hi');"""

# Insert the multi-goal aggregator inside generateCoachMission (above compileMissionData)
target_insertion = "      // Helper function to build predictions for a specific language\n      function compileMissionData(lang) {"
new_insertion = multi_goal_func + "\n" + target_insertion

if target_insertion in content:
    content = content.replace(target_insertion, new_insertion, 1)
    print("Injected compileMultiGoalMissionData successfully.")
else:
    print("ERROR: target_insertion not found!")

if old_calls in content:
    content = content.replace(old_calls, new_calls, 1)
    print("Updated calls successfully.")
else:
    print("ERROR: old_calls not found!")

# 2. Update unifiedVedicText generation
old_unified_block = """      const lordDetails = currentAppLang === 'hi' ? (vedicMantrasHi[rulingLord] || vedicMantrasHi["Sun"]) : (vedicMantrasEn[rulingLord] || vedicMantrasEn["Sun"]);
      // Build goal-specific ritual text for the dashboard quest card
      const _contextMap = currentAppLang === 'hi' ? (() => { const m = { job: 'करियर और अधिकार के स्पंदनों को सक्रिय करने के लिए सूर्योदय से पहले सूर्य नमस्कार (12 चक्र) करें।', debt: 'वित्तीय चिंताओं को दूर करने के लिए भोजन से पहले 108 बार "ॐ नमः शिवाय" का जाप करें।', marriage: 'अपने भाग्यशाली जीवनसाथी को आकर्षित करने के लिए शुक्रवार की सुबह कात्यायनी मंत्र का 108 बार जाप करें।', baby: 'संतान सुख के लिए प्रत्येक सुबह 108 बार संतान गोपाल मंत्र का जाप करें।', business: 'बुधवार को गणेश पूजा करें और अपने व्यावसायिक प्रवेश द्वार पर धूप जलाएं।', property: 'संपत्ति के दौरों से पहले "ॐ भौमाय नमः" का 11 बार जाप करें।', health: 'सूर्योदय के समय सूर्य नमस्कार करें और जीवन शक्ति के लिए तांबे के बर्तन का पानी पिएं।', custom: 'शाम को घी के दीये के साथ पूजा करें और अपने लक्ष्य पर ध्यान केंद्रित करें।' }; return m; })() : { job: 'Perform Surya Namaskaar (12 rounds) before sunrise to activate career and authority vibrations.', debt: 'Recite "Om Namah Shivaya" 108 times before meals to dissolve financial anxieties.', marriage: 'Recite the Katyayani mantra 108 times on Friday morning to attract your destined partner.', baby: 'Recite the Santan Gopal mantra 108 times each morning for progeny blessings.', business: 'Perform Ganesh puja on Wednesdays and light incense at your business entrance.', property: 'Chant "Om Bhaumaya Namah" 11 times before property visits for Mars blessings.', health: 'Perform Surya Namaskar at sunrise and drink copper vessel water in the morning for vitality.', custom: 'Perform an evening puja with incense and a ghee lamp, focusing intention on your goal.' };
      const _nGoal = normalizedGoal in _contextMap ? normalizedGoal : 'custom';
      const _goalRitual = _contextMap[_nGoal] || _contextMap['custom'];
      const unifiedVedicText = currentAppLang === 'hi'
        ? `शासक ग्रह मंत्र: "${lordDetails.mantra}" का 108 बार जाप करें (लक्ष्य: ${activeGoalNames})। पवित्र पाठ: ${lordDetails.text} लक्ष्य अनुष्ठान: ${_goalRitual}`
        : `Ruling Planet Mantra: Chant "${lordDetails.mantra}" 108 times each morning facing East. (Goal: ${activeGoalNames}). Sacred Text: ${lordDetails.text} Goal Ritual: ${_goalRitual}`;
      localStorage.setItem('today_quest_vedic_text', unifiedVedicText);"""

new_unified_block = """      const lordDetails = currentAppLang === 'hi' ? (vedicMantrasHi[rulingLord] || vedicMantrasHi["Sun"]) : (vedicMantrasEn[rulingLord] || vedicMantrasEn["Sun"]);
      // Build goal-specific ritual text for the dashboard quest card
      const _contextMap = currentAppLang === 'hi' ? {
        job: 'करियर और अधिकार के स्पंदनों को सक्रिय करने के लिए सूर्योदय से पहले सूर्य नमस्कार (12 चक्र) करें।',
        debt: 'वित्तीय चिंताओं को दूर करने के लिए भोजन से पहले 108 बार "ॐ नमः शिवाय" का जाप करें।',
        marriage: 'अपने भाग्यशाली जीवनसाथी को आकर्षित करने के लिए शुक्रवार की सुबह कात्यायनी मंत्र का 108 बार जाप करें।',
        baby: 'संतान सुख के लिए प्रत्येक सुबह 108 बार संतान गोपाल मंत्र का जाप करें।',
        business: 'बुधवार को गणेश पूजा करें और अपने व्यावसायिक प्रवेश द्वार पर धूप जलाएं।',
        property: 'संपत्ति के दौरों से पहले "ॐ भौमाय नमः" का 11 बार जाप करें।',
        health: 'सूर्योदय के समय सूर्य नमस्कार करें और जीवन शक्ति के लिए तांबे के बर्तन का पानी पिएं।',
        custom: 'शाम को घी के दीये के साथ पूजा करें और अपने लक्ष्य पर ध्यान केंद्रित करें।'
      } : {
        job: 'Perform Surya Namaskaar (12 rounds) before sunrise to activate career and authority vibrations.',
        debt: 'Recite "Om Namah Shivaya" 108 times before meals to dissolve financial anxieties.',
        marriage: 'Recite the Katyayani mantra 108 times on Friday morning to attract your destined partner.',
        baby: 'Recite the Santan Gopal mantra 108 times each morning for progeny blessings.',
        business: 'Perform Ganesh puja on Wednesdays and light incense at your business entrance.',
        property: 'Chant "Om Bhaumaya Namah" 11 times before property visits for Mars blessings.',
        health: 'Perform Surya Namaskar at sunrise and drink copper vessel water in the morning for vitality.',
        custom: 'Perform an evening puja with incense and a ghee lamp, focusing intention on your goal.'
      };

      const ritualsList = [];
      activeGoalsList.forEach(g => {
        let nG = g;
        if (g === 'marriage-single' || g === 'marriage-couple') nG = 'marriage';
        if (g === 'property-single' || g === 'property-couple') nG = 'property';
        const targetRitualKey = nG in _contextMap ? nG : 'custom';
        const ritualText = _contextMap[targetRitualKey] || _contextMap['custom'];
        const label = (currentAppLang === 'hi' ? (goalLabelsHi[g] || goalLabelsEn[g] || g) : (goalLabelsEn[g] || g));
        ritualsList.push(`[${label}]: ${ritualText}`);
      });
      const combinedGoalRitualsText = ritualsList.join(" ");

      const unifiedVedicText = currentAppLang === 'hi'
        ? `शासक ग्रह मंत्र: "${lordDetails.mantra}" का 108 बार जाप करें (लक्ष्य: ${activeGoalNames})। पवित्र पाठ: ${lordDetails.text} लक्ष्य अनुष्ठान: ${combinedGoalRitualsText}`
        : `Ruling Planet Mantra: Chant "${lordDetails.mantra}" 108 times each morning facing East. (Goals: ${activeGoalNames}). Sacred Text: ${lordDetails.text} Goal Rituals: ${combinedGoalRitualsText}`;
      localStorage.setItem('today_quest_vedic_text', unifiedVedicText);"""

if old_unified_block in content:
    content = content.replace(old_unified_block, new_unified_block, 1)
    print("Updated unifiedVedicText block successfully.")
else:
    print("WARNING: Exact old_unified_block not found. Trying flexible replacement...")
    start_str = "const lordDetails = currentAppLang === 'hi' ? (vedicMantrasHi[rulingLord] || vedicMantrasHi[\"Sun\"])"
    end_str = "localStorage.setItem('today_quest_vedic_text', unifiedVedicText);"
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        before = content[:start_idx]
        after = content[end_idx + len(end_str):]
        content = before + new_unified_block + after
        print("Flexible replacement of unifiedVedicText block succeeded!")
    else:
        print("ERROR: Flexible replacement of unifiedVedicText block failed!")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Finished writing index.html.")
