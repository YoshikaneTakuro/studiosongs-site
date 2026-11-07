// studiosongs.net（wwwなし）を www.studiosongs.net へ統一し、それ以外は静的ファイルを返す
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "studiosongs.net") {
      url.hostname = "www.studiosongs.net";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
