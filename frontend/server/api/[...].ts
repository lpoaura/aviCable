/* global defineEventHandler, useRuntimeConfig */
/* eslint no-console: ["error", { allow: ["warn","debug","error"] }] */

import { createError, readBody, appendHeader, defineEventHandler } from "h3";

export default defineEventHandler(async (event) => {
  console.debug("API [...].ts");
  const config = useRuntimeConfig();
  if (!config.public.apiBase) {
    throw new Error("Missing `runtimeConfig.apiBase` configuration.");
  }
  const { method, url, headers } = event.req;
  const body = method !== "GET" && method !== "HEAD" ? await readBody(event) : undefined;
  console.log(    "API Service method",    method)
  console.log(    "baseUrl",    config.public.apiBase)
  console.log(    'url',    url)
  console.log(    "headers",    headers)


  try {
    const response = await $fetch.raw(url, {
      method,
      baseURL: config.public.apiBase,
      headers,
      body,
    });

    for (const header of ["set-cookie", "cache-control"]) {
      if (response.headers.has(header)) {
        appendHeader(event, header, response.headers.get(header));
      }
    }

    return response._data;
  } catch (error) {
    console.error(error);
    // return createError({
    //   statusCode: error.response.status,
    //   statusMessage: error.message,
    //   data: error.data
    // })
  }
});
