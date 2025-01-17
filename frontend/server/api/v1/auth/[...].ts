// server/api/[...].ts
import { createError, readBody, appendHeader, defineEventHandler } from "h3";
// import { useRuntimeConfig } from '#app'; // Import useRuntimeConfig to access runtime configuration

export default defineEventHandler(async (event) => {
  console.debug("API [...].ts");

  const config = useRuntimeConfig();
  if (!config.public.baseURL) {
    throw new Error("Missing `runtimeConfig.baseURL` configuration.");
  }

  const { method, url, headers } = event.req;
  console.log('event',event)
  const body = method !== "GET" && method !== "HEAD" ? await readBody(event) : undefined;

  console.log("API Service method", method);
  console.log("baseURL", config.public.baseURL);
  console.log('url', url);
  console.log("headers", headers);
  console.log('body', body)

  try {
    console.log('try fetch')
    const response = await $fetch.raw(url, {
      method,
      baseURL: config.public.baseURL,
      headers,
      body,
    });
    console.log('response', response)
    for (const header of ["set-cookie", "cache-control"]) {
      if (response.headers.has(header)) {
        appendHeader(event, header, response.headers.get(header));
      }
    }

    return response._data;
  } catch (error) {
    console.error(error);
    return createError({
      statusCode: error.response?.status || 500,
      statusMessage: error.message,
      data: error.data || null,
    });
  }
});
