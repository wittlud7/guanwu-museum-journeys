async page=>{
 const assert=(value,message)=>{if(!value)throw Error(message)},errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://localhost:4173/index.html?verify='+Date.now()+'#collection');
 await page.waitForFunction(()=>document.querySelector('main')?.dataset.route==='collection');
 assert(await page.locator('.museum-card').count()===11,'11 museums');
 assert(await page.locator('.craft-card a[href^="#artifact/"]').count()===36,'18 artifacts (cover and title)');
 await page.locator('#collection-search').fill('勾践');assert(await page.locator('.craft-card').count()===1,'artifact search');
 await page.locator('a[href="#artifact/goujian-sword"]').first().click();await page.waitForFunction(()=>document.querySelector('main')?.dataset.route==='artifact/goujian-sword');
 await page.locator('.craft-main-image img').evaluate(i=>i.decode());
 await page.locator('[data-companion]').first().click();await page.waitForFunction(()=>document.querySelector('.companion-status').textContent.includes('已连接'));
 await page.locator('#companion-input').fill('用简短文字给8岁孩子讲这件文物，附来源。');await page.locator('.companion-send').click();
 await page.waitForFunction(()=>document.querySelector('.companion')?.getAttribute('aria-busy')==='false',{},{timeout:60000});
 assert((await page.locator('.companion-message.assistant').last().innerText()).length>50,'live answer');assert(await page.locator('.companion-references a').count()>0,'live sourced response');
 await page.locator('#companion-input').fill('请建议将湖北省博物馆加入我的行程。');await page.locator('.companion-send').click();
 await page.waitForFunction(()=>document.querySelector('.companion')?.getAttribute('aria-busy')==='false',{},{timeout:60000});
 const confirm=page.locator('.companion-message.assistant .outline-btn');assert(await confirm.count()===1,'tool proposal');
 const before=await page.evaluate(()=>JSON.parse(localStorage.getItem('guanwu-plan-v2')||'[]').includes('wuhan'));
 await confirm.click();assert(await page.evaluate(()=>JSON.parse(localStorage.getItem('guanwu-plan-v2')||'[]').includes('wuhan')),'confirmed itinerary action');
 await page.locator('.companion-close').click();
 for(const width of [360,390,768,1440]){await page.setViewportSize({width,height:900});for(const hash of ['museum/xian','museum/wuhan','artifact/goujian-sword','artifact/vermilion-coffin','saved']){await page.evaluate(h=>location.hash=h,hash);await page.waitForFunction(h=>document.querySelector('main')?.dataset.route===h,hash);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+width+hash)}}
 await page.goto('http://localhost:4173/mini.html');const frame=page.frameLocator('iframe');await frame.locator('main h1').waitFor();await page.getByRole('button',{name:'博物馆',exact:true}).click();await frame.locator('#collection-search').waitFor();await frame.locator('#collection-search').fill('玛瑙');assert(await frame.locator('.craft-card').count()===1,'mini preview search');assert(!errors.length,errors.join(';'));
 await page.screenshot({path:'output/mini-preview.png',fullPage:true});
 return {status:'PASS',museums:11,artifacts:18,liveDeepSeek:true,sourcedAnswer:true,confirmedJourney:true,preexistingJourney:before,responsiveWidths:[360,390,768,1440],miniPreview:true};
}
