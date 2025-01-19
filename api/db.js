import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export async function saveWhopData(data) {
  const { platform_metrics, top_communities } = data
  
  return await prisma.whopData.create({
    data: {
      totalRevenue: platform_metrics.total_revenue,
      totalUsers: platform_metrics.total_users,
      communities: {
        create: top_communities.map(c => ({
          name: c.name,
          pricePerUnit: c.price_per_unit,
          logo: c.logo,
          title: c.title,
          otherInformation: c.other_information,
          whopRank: c.whop_rank,
          affiliateEarnings: c.affiliate_earnings,
          rank: c.rank
        }))
      }
    }
  })
}

export async function getLatestWhopData() {
  return await prisma.whopData.findFirst({
    include: {
      communities: true
    },
    orderBy: {
      createdAt: 'desc'
    }
  })
}
