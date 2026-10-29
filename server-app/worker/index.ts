import handler from "vinext/server/fetch-handler";
import { handleGuide } from '../lib/guide.mjs';
import { handleKnowledge } from '../lib/knowledge.mjs';
import catalog from '../lib/catalog.json';
import { handleCommunity } from '../lib/community.mjs';
import { runWithConnectorBinding } from "../lib/connector-context";
import type { ConnectorBinding } from "../lib/connector-contract.mjs";
const guideWindows = new Map<string, {count:number;start:number}>();

const worker = {
  fetch(request: Request, env: Cloudflare.Env, ctx: ExecutionContext<{ CONNECTORS?: ConnectorBinding }>) {
    if(new URL(request.url).pathname.startsWith('/api/community/'))return handleCommunity(request,env,catalog);
    if (new URL(request.url).pathname.startsWith('/api/guide')||new URL(request.url).pathname.startsWith('/api/knowledge')) {
      if(request.method==='POST') {
        const now=Date.now(),key=request.headers.get('oai-authenticated-user-id')||request.headers.get('cf-connecting-ip')||'anonymous';
        let window=guideWindows.get(key);if(!window||now-window.start>=60_000){window={count:0,start:now};guideWindows.set(key,window)}
        if(++window.count>10)return Response.json({error:'提问有些密集，请稍等一分钟，让这次观看慢一点。'},{status:429,headers:{'Cache-Control':'no-store','Retry-After':'60'}});
        if(guideWindows.size>2000)for(const [id,value] of guideWindows)if(now-value.start>=60_000)guideWindows.delete(id);
      }
      return new URL(request.url).pathname.startsWith('/api/knowledge')?handleKnowledge(request,env,catalog):handleGuide(request, env, catalog);
    }
    let binding = ctx.props?.CONNECTORS;
    // Local preview emulates the same request-scoped capability. This branch and
    // the auxiliary service binding are absent from production builds.
    if (import.meta.env.DEV && !binding && env.CONNECTORS) {
      const preview = env.CONNECTORS;
      const expiresAt = Date.now() + 60_000;
      binding = {
        async getContext() {
          if (Date.now() >= expiresAt) return { status: "request_context_expired" };
          return preview.getContext?.() ?? { status: "binding_unavailable" };
        },
        async invoke(connectorId, actionName, args) {
          if (Date.now() >= expiresAt) {
            return { status: "request_context_expired", message: "This request has expired. Please try again." };
          }
          return preview.invoke(connectorId, actionName, args);
        },
      };
    }
    return runWithConnectorBinding(binding, () => handler.fetch(request, env, ctx));
  },
};

export default worker;
