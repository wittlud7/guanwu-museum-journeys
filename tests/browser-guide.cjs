async (page) => {
 const check=(v,m)=>{if(!v)throw Error(m)},errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const base='http://localhost:4173/';
 const go=async hash=>{await page.goto(base+'#'+hash);await page.waitForFunction(h=>document.querySelector('main')?.dataset.route===h,hash);await page.locator('main h1').waitFor()};
 await page.setViewportSize({width:390,height:844});await page.goto(base+'?qa='+Date.now()+'#discover');await go('discover');
 await page.evaluate(async()=>{localStorage.clear();for(const r of await navigator.serviceWorker.getRegistrations())await r.unregister();for(const k of await caches.keys())if(k.startsWith('guanwu-'))await caches.delete(k)});
 await page.reload();await page.locator('.museum-card').first().waitFor();
 check(await page.locator('.museum-card').count()===11,'首页十一座馆');
 await page.getByRole('button',{name:'查看广州精选',exact:true}).click();
 check((await page.locator('.heritage-hero').getAttribute('aria-label')).includes('粤剧'),'切换广州头图');
 await page.locator('[data-city="杭州"]').click();check(await page.locator('.museum-card').count()===1,'杭州筛选');
 await page.locator('[data-city="全部"]').click();await page.getByRole('link',{name:'博物馆',exact:true}).click();
 await page.locator('#collection-search').fill('云锦');check(await page.locator('.museum-card').count()===1,'云锦场馆搜索');check(await page.locator('.craft-card').count()===1,'云锦工艺搜索');
 await page.locator('#collection-search').fill('火星不存在');check(await page.getByText('暂时没有找到这段故事').isVisible(),'空状态');
 await page.getByRole('button',{name:'重新发现 →',exact:true}).click();
 await page.locator('.museum-card a[href="#museum/nanjing"]').first().click();await page.getByRole('heading',{name:'南京云锦博物馆',exact:true}).waitFor();
 check(await page.getByText('南京市建邺区茶亭东街240号',{exact:true}).isVisible(),'真实地址');
 await page.locator('.museum-main-image').click();check(await page.locator('#gallery').isVisible(),'图片浏览器');
 await page.getByRole('button',{name:'放大图片',exact:true}).click();check(await page.locator('#zoom-label').textContent()==='150%','放大图片');
 await page.keyboard.press('ArrowRight');check((await page.locator('#gallery-image').getAttribute('src')).includes('nanjing-loom'),'键盘切图');
 check((await page.locator('.gallery-bottom').textContent()).includes('CC BY-SA'),'照片许可可见');await page.keyboard.press('Escape');
 await page.getByRole('button',{name:'▷ 听一听这座馆',exact:true}).click();
 await page.waitForFunction(()=>{const a=document.querySelector('audio');return a.duration>10&&a.currentTime>.2&&!a.paused});
 await page.getByRole('button',{name:'暂停导览',exact:true}).click();check(await page.locator('audio').evaluate(a=>a.paused),'真实音频暂停');
 await page.locator('#audio-seek').evaluate(input=>{input.value=11;input.dispatchEvent(new Event('input',{bubbles:true}));input.dispatchEvent(new Event('change',{bubbles:true}))});
 check(await page.locator('audio').evaluate(a=>Math.abs(a.currentTime-11)<1),'进度拖动');
 await page.locator('#audio-rate').selectOption('1.2');check(await page.locator('audio').evaluate(a=>a.playbackRate===1.2),'真实倍速');
 await page.getByRole('link',{name:'城市漫游',exact:true}).click();await page.getByRole('heading',{name:'给一座城，多一点时间',exact:true}).waitFor();
 check(await page.locator('audio').count()===1,'导航不创建重复音频');check(await page.locator('#audio-dock').isVisible(),'跨页保留播放器');
 await go('museum/nanjing');await page.getByRole('button',{name:'关闭播放器',exact:true}).click();
 await page.locator('[data-play="museum:nanjing:1"]').click();check(await page.locator('#modal').isVisible(),'深度导览门槛');
 await page.getByRole('button',{name:'免费体验全部导览 →',exact:true}).click();
 await page.locator('[data-play="museum:nanjing:1"]').click();await page.waitForFunction(()=>document.querySelector('audio').currentTime>.1);
 check((await page.locator('audio').getAttribute('src')).includes('nanjing-1'),'第二章真实音频');
 await page.getByRole('button',{name:'暂停导览',exact:true}).click();
 await page.getByRole('button',{name:'查看当前讲解文稿',exact:true}).click();check((await page.locator('#modal').textContent()).includes('传统云锦织造'),'音频文稿');await page.keyboard.press('Escape');
 await page.locator('.heading-buttons [data-save]').click();await page.locator('#note-input').fill('在织机前，先看两个人的配合，再看经纬。');await page.getByRole('button',{name:'保存手记 ↗',exact:true}).click();
 await page.locator('[data-plan="nanjing"]').click();await go('museum/beijing');await page.locator('[data-plan="beijing"]').click();
 await go('saved');check(await page.locator('.plan-row').count()===2,'多馆行程');
 await page.locator('[data-date="nanjing"]').fill('2026-11-01');await page.locator('[data-move="beijing:-1"]').click();
 check((await page.locator('.plan-row').first().textContent()).includes('中国工艺美术馆'),'行程排序');
 await page.reload();await page.locator('.plan-row').first().waitFor();check(await page.locator('[data-date="nanjing"]').inputValue()==='2026-11-01','日期持久化');
 check((await page.locator('.journal-note').textContent()).includes('经纬'),'手记持久化');
 await go('craft/yunjin');await page.locator('.quiz-invite').click();await page.locator('[data-answer="yunjin:0"]').click();check((await page.locator('#quiz-feedback').textContent()).includes('再想一想'),'答错可重试');
 await page.locator('[data-answer="yunjin:1"]').click();check((await page.locator('#quiz-feedback').textContent()).includes('知识印记'),'答对取得印记');await page.keyboard.press('Escape');
 await go('saved');check(await page.locator('.stamp.earned').count()===1,'印记持久化');
 // All representative views, at four widths, must load real media without overflow.
 for(const width of [360,390,768,1280]){
  await page.setViewportSize({width,height:844});
  for(const hash of ['discover','collection','crafts','journeys','saved',...['beijing','hangzhou','nanjing','chengdu','guangzhou'].map(id=>'museum/'+id),'craft/cloisonne','craft/shuxiu','craft/cantonese-opera']){
   await go(hash);await page.locator('img').evaluateAll(async imgs=>{imgs.forEach(i=>i.loading='eager');await Promise.all(imgs.map(i=>i.decode().catch(()=>{})))});
   check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`横向溢出 ${width} ${hash}`);
   check(await page.locator('img').evaluateAll(imgs=>imgs.every(i=>i.naturalWidth>0)),`图片损坏 ${width} ${hash}`);
  }
 }
 await page.setViewportSize({width:390,height:844});await go('museum/beijing');
 await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
 await page.getByRole('button',{name:'↓ 保存本馆离线导览',exact:true}).click();
 await page.locator('[data-download-status="beijing"]').filter({hasText:'已保存'}).waitFor();
 await page.context().setOffline(true);await page.reload();await page.getByRole('heading',{name:'中国工艺美术馆 · 中国非遗馆',exact:true}).waitFor();
 await page.getByRole('button',{name:'▷ 听一听这座馆',exact:true}).click();await page.waitForFunction(()=>document.querySelector('audio').currentTime>.2);
 check(await page.locator('audio').evaluate(a=>!a.error),'断网音频可播');
 await page.context().setOffline(false);await page.getByRole('button',{name:'关闭播放器',exact:true}).click();
 check(errors.length===0,'JS错误：'+errors.join(','));
 await page.screenshot({path:'output/playwright/heritage-museum-mobile.png',fullPage:true});
 await go('discover');await page.screenshot({path:'output/playwright/heritage-home-mobile.png',fullPage:true});
 return {status:'passed',museumCities:11,craftTopics:8,widths:[360,390,768,1280],routesPerWidth:13,offlineAudio:true,search:true,gallery:true,notes:true,itinerary:true,quiz:true,javascriptErrors:errors};
}
