export default {
	async fetch(request) {
	  const reqUrl = new URL(request.url);
	  const raw = decodeURIComponent(reqUrl.pathname.slice(1));
  
	  if (!raw.startsWith('vless://')) {
		return new Response('invalid vless url', { status: 400 });
	  }
  
	  /* ========= 控制参数 ========= */
	  const baseName = reqUrl.searchParams.get('name') || 'base';
	  const remark = reqUrl.searchParams.get('remark') || '';
	  const prefix = remark ? `[${remark}] ` : '';
  
	  /* ========= 拆 VLESS（不用 URL）========= */
	  const m = raw.match(
		/^vless:\/\/([^@]+)@([^:/?#]+)(?::(\d+))?(\?[^#]*)?$/
	  );
	  if (!m) return new Response('bad vless format', { status: 400 });
  
	  const [, uuid, host, port = '443', vlessQuery = ''] = m;
  
	  /* ========= 合并 query（关键）========= */
	  const merged = new URLSearchParams(
		vlessQuery.startsWith('?') ? vlessQuery.slice(1) : ''
	  );
  
	  // 把 Worker URL 的 query 注入 VLESS
	  for (const [k, v] of reqUrl.searchParams.entries()) {
		if (k === 'name' || k === 'remark') continue; // 控制字段
		merged.set(k, v);
	  }
  
	  const finalQuery = merged.toString()
		? '?' + merged.toString()
		: '';
  
	  const nodes = [];
  
	  /* ========= 原始节点 ========= */
	  nodes.push(
		`vless://${uuid}@${host}:${port}${finalQuery}#${encodeURIComponent(prefix + baseName)}`
	  );
  
	  /* ========= 优选 API ========= */
	  const apis = [
		'https://cf.001315.xyz/ip.164746.xyz',
		'https://cf.001315.xyz/CloudFlareYes',
		'https://cf.001315.xyz/CM/ct',
		'https://cf.001315.xyz/CM/cmcc'
	  ];
  
	  const seen = new Set();
  
	  for (const api of apis) {
		try {
		  const res = await fetch(api);
		  const text = await res.text();
  
		  for (const line of text.split('\n')) {
			const [ip, name] = line.split('#').map(s => s?.trim());
			if (!ip || !name || seen.has(ip)) continue;
  
			seen.add(ip);
  
			nodes.push(
			  `vless://${uuid}@${ip}:${port}${finalQuery}#${encodeURIComponent(prefix + name)}`
			);
		  }
		} catch {}
	  }
  
	  return new Response(nodes.join('\n'), {
		headers: { 'content-type': 'text/plain; charset=utf-8' }
	  });
	}
  };
  
