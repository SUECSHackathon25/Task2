import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */

  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Clacks-Overhead',
            value: 'GNU Terry Pratchett',
          },
        ],
      },
    ]
  },
};

export default nextConfig;
