"""Build selectable, disclosed AI Mandarin audio using Microsoft Edge neural TTS.

Reuses our authored guide text exactly. No visitor text or credentials are sent.
Run --previews first, then without arguments. Finished jobs are fingerprint-cached.
"""
import argparse
import asyncio
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.runtime'))
import edge_tts

OUT = ROOT / 'dist/assets/audio'
PACKS = [
    dict(id='xiaoxiao', name='温润讲述', description='柔和女声，舒缓地陪你看展。', voice='zh-CN-XiaoxiaoNeural', rate='-8%', pitch='+0Hz', pathPrefix='assets/audio'),
    dict(id='yunxi', name='沉静男声', description='清朗男声，节奏从容、层次清晰。', voice='zh-CN-YunxiNeural', rate='-10%', pitch='+0Hz', pathPrefix='assets/audio/packs/yunxi'),
    dict(id='xiaoyi', name='清亮女声', description='明亮女声，语速适中、咬字清楚。', voice='zh-CN-XiaoyiNeural', rate='-6%', pitch='+0Hz', pathPrefix='assets/audio/packs/xiaoyi'),
]
PREVIEW_TEXT = '欢迎来到观物。选一种你喜欢的声音，慢慢走近眼前的作品。先看材料，再看细节。让好奇心，决定你的下一站。'


def jobs():
    data = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./dist/heritage-data.js')))"], cwd=ROOT, encoding='utf-8'))
    result = [dict(id=f"{m['id']}-{i}", title=c['title'], text=c['text']) for m in data['museums'] for i, c in enumerate(m['chapters'])]
    result += [dict(id='craft-' + c['id'], title=c['title'], text=c['audioText']) for c in data['crafts']]
    assert len(result) == 23
    return result


async def render(job, pack, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    timing = dest.with_suffix('.json')
    fingerprint = hashlib.sha256((job['text'] + pack['voice'] + pack['rate'] + pack['pitch']).encode()).hexdigest()
    if dest.exists() and timing.exists() and json.loads(timing.read_text(encoding='utf-8')).get('hash') == fingerprint:
        print('CACHED', pack['id'], job['id'], flush=True)
        return
    for attempt in range(3):
        try:
            comm = edge_tts.Communicate(job['text'], pack['voice'], rate=pack['rate'], pitch=pack['pitch'], boundary='SentenceBoundary')
            boundaries = []
            tmp = dest.with_suffix('.part')
            with tmp.open('wb') as stream:
                async for chunk in comm.stream():
                    if chunk['type'] == 'audio':
                        stream.write(chunk['data'])
                    elif chunk['type'] in ('WordBoundary', 'SentenceBoundary'):
                        boundaries.append(dict(start=round(chunk['offset'] / 1e7, 3), end=round((chunk['offset'] + chunk['duration']) / 1e7, 3), text=chunk['text']))
            assert tmp.stat().st_size > 3000 and boundaries, 'Missing audio or sentence timings'
            tmp.replace(dest)
            timing.write_text(json.dumps(dict(hash=fingerprint, voice=pack['voice'], rate=pack['rate'], pitch=pack['pitch'], synthetic=True, provider='Microsoft Edge neural TTS via edge-tts', text=job['text'], sentences=boundaries), ensure_ascii=False, indent=2), encoding='utf-8')
            print('OK', pack['id'], job['id'], dest.stat().st_size, flush=True)
            return
        except Exception as error:
            print('RETRY', pack['id'], job['id'], type(error).__name__, flush=True)
            if attempt == 2:
                raise
            await asyncio.sleep(3 + attempt * 4)


def heritage_jobs():
    path = ROOT / 'dist/world-heritage-data.js'
    if not path.exists():
        return []
    data = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./dist/world-heritage-data.js')))"], cwd=ROOT, encoding='utf-8'))
    sites = data.get('sites', data.get('items', []))
    return [dict(id=s['id'], title=s.get('title') or s['name'], text=s.get('narrationText') or s['intro']) for s in sites]


def normalize_audio():
    """Equalize pack loudness with two-pass EBU R128, preserving clip timing."""
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    paths = [OUT / (j['id'] + '.mp3') for j in jobs()]
    paths += list((OUT / 'packs').rglob('*.mp3')) if (OUT / 'packs').exists() else []
    paths += list((OUT / 'heritage').glob('*.mp3')) if (OUT / 'heritage').exists() else []
    paths += list((OUT / 'previews').glob('*.mp3'))
    for path in sorted(set(paths)):
        if path.name.endswith('.normalized.mp3'):
            continue
        timing = path.with_suffix('.json')
        data = json.loads(timing.read_text(encoding='utf-8'))
        if data.get('audioProcessing') == 'EBU R128 I=-18 LUFS TP=-1.5 dBTP LRA=11 two-pass':
            continue
        first = subprocess.run([ffmpeg, '-hide_banner', '-i', str(path), '-af', 'loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
        values = json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}', first.stderr).group())
        settings = ':'.join(['loudnorm=I=-18:TP=-1.5:LRA=11', 'measured_I=' + values['input_i'], 'measured_TP=' + values['input_tp'], 'measured_LRA=' + values['input_lra'], 'measured_thresh=' + values['input_thresh'], 'offset=' + values['target_offset'], 'linear=true'])
        temp = path.with_name(path.stem + '.normalized.mp3')
        subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(path), '-af', settings, '-ar', '24000', '-ac', '1', '-b:a', '48k', str(temp)], capture_output=True, check=True)
        temp.replace(path)
        data['audioProcessing'] = 'EBU R128 I=-18 LUFS TP=-1.5 dBTP LRA=11 two-pass'
        timing.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print('NORMALIZED', path.relative_to(OUT).as_posix(), flush=True)


def verify_audio():
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    core = jobs()
    heritage = heritage_jobs()
    expected = []
    for pack in PACKS:
        expected += [(ROOT / 'dist' / pack['pathPrefix'] / (j['id'] + '.mp3'), j, pack) for j in core]
        expected += [(ROOT / 'dist' / pack['pathPrefix'] / 'heritage' / (j['id'] + '.mp3'), j, pack) for j in heritage]
        expected.append((OUT / 'previews' / (pack['id'] + '.mp3'), dict(text=PREVIEW_TEXT), pack))
    result = []
    for path, job, pack in expected:
        data = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
        assert data['text'] == job['text'] and data['voice'] == pack['voice'] and data['rate'] == pack['rate'], path
        assert data['sentences'] and all(s['end'] > s['start'] >= 0 for s in data['sentences']), path
        decoded = subprocess.run([ffmpeg, '-hide_banner', '-i', str(path), '-af', 'loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
        values = json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}', decoded.stderr).group())
        assert abs(float(values['input_i']) + 18) <= 1.1, (path, values)
        assert float(values['input_tp']) < -.3, (path, values)
        duration = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', decoded.stderr)
        hours, minutes, seconds = map(float, duration.groups())
        duration = hours * 3600 + minutes * 60 + seconds
        assert data['sentences'][-1]['end'] < duration + .2, (path, duration)
        result.append(dict(path=path.relative_to(ROOT / 'dist').as_posix(), bytes=path.stat().st_size, duration=duration, integratedLUFS=float(values['input_i']), truePeakDBTP=float(values['input_tp']), voice=pack['voice']))
    (ROOT / 'research/voice-packs-measurements.json').write_text(json.dumps(dict(clips=len(result), totalBytes=sum(r['bytes'] for r in result), measurements=result), ensure_ascii=False, indent=2), encoding='utf-8')
    print('VERIFIED', len(result), 'clips;', len(core), 'core x 3;', len(heritage), 'heritage x 3; previews 3', flush=True)


async def main(previews_only=False, heritage_only=False):
    voices = {v['ShortName'] for v in await edge_tts.list_voices()}
    assert all(p['voice'] in voices for p in PACKS), 'Required voice unavailable'
    work = jobs()
    for pack in PACKS:
        await render(dict(id='preview', text=PREVIEW_TEXT), pack, OUT / 'previews' / (pack['id'] + '.mp3'))
        await asyncio.sleep(.7)
    if previews_only:
        return
    if not heritage_only:
        for pack in PACKS[1:]:
            for job in work:
                await render(job, pack, ROOT / 'dist' / pack['pathPrefix'] / (job['id'] + '.mp3'))
                await asyncio.sleep(.7)
            (ROOT / 'dist' / pack['pathPrefix'] / 'manifest.json').write_text(json.dumps(dict(provider='Microsoft Edge neural TTS via edge-tts', voice=pack['voice'], rate=pack['rate'], pitch=pack['pitch'], disclosure='AI 合成普通话导览，非真人录音或声音克隆', jobs=work), ensure_ascii=False, indent=2), encoding='utf-8')
    heritage = heritage_jobs()
    if heritage_only:
        assert len(heritage) == 46, 'Expected all 46 cultural and mixed sites'
    semaphore = asyncio.Semaphore(2)
    async def render_heritage(job, pack):
        async with semaphore:
            await render(job, pack, ROOT / 'dist' / pack['pathPrefix'] / 'heritage' / (job['id'] + '.mp3'))
            await asyncio.sleep(.7)
    await asyncio.gather(*(render_heritage(job, pack) for pack in PACKS for job in heritage))
    for pack in PACKS:
        if heritage:
            (ROOT / 'dist' / pack['pathPrefix'] / 'heritage/manifest.json').write_text(json.dumps(dict(provider='Microsoft Edge neural TTS via edge-tts', voice=pack['voice'], rate=pack['rate'], pitch=pack['pitch'], disclosure='AI 合成普通话导览，非真人录音或声音克隆', jobs=heritage), ensure_ascii=False, indent=2), encoding='utf-8')
    payload = dict(default='xiaoxiao', provider='Microsoft Edge neural TTS via edge-tts', disclosure='AI 合成普通话导览，非真人录音或声音克隆', audioProcessing='EBU R128 I=-18 LUFS TP=-1.5 dBTP LRA=11 two-pass', encoding='MP3 24000 Hz mono 48 kbps', packs=[dict(**p, preview='assets/audio/previews/' + p['id'] + '.mp3', tracks=len(work), heritageTracks=len(heritage)) for p in PACKS])
    (ROOT / 'dist/voice-packs-data.js').write_text("(function(root,factory){if(typeof module==='object'&&module.exports){module.exports=factory();}else{root.GUANWU_VOICE_PACKS=factory();}})(typeof self!=='undefined'?self:this,function(){return " + json.dumps(payload, ensure_ascii=False, indent=2) + ';});\n', encoding='utf-8')
    normalize_audio()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--previews', action='store_true')
    parser.add_argument('--heritage-only', action='store_true')
    parser.add_argument('--normalize-only', action='store_true')
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    if args.verify:
        verify_audio()
    elif args.normalize_only:
        normalize_audio()
    else:
        asyncio.run(main(args.previews, args.heritage_only))
