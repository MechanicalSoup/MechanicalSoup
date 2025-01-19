export interface WhopCommunity {
  name: string;
  price_per_unit: string;
  logo: string;
  title: string;
  other_information: string;
  whop_rank: string;
  affiliate_earnings: string;
  rank: number;
}

export interface PlatformMetrics {
  total_revenue: string;
  total_users: string;
}

export interface WhopData {
  platform_metrics: PlatformMetrics;
  top_communities: WhopCommunity[];
}
