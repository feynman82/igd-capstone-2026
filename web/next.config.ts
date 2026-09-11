import type { NextConfig } from "next";

/**
 * The interface never talks to the database and never talks to another origin.
 *
 * Every call to the local API goes through a route handler under `app/api/`, which is why
 * `api/main.py` ships no CORS middleware: from the API's point of view there is exactly one
 * client, on 127.0.0.1, arriving same-origin. The address of that API is the only thing this
 * file needs to know, and it is read at request time rather than baked into the bundle so a
 * person can move the port without a rebuild.
 */
const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "no-referrer" },
          // An offline household tool has no business in anyone's frame.
          { key: "X-Frame-Options", value: "DENY" },
        ],
      },
    ];
  },
};

export default nextConfig;
