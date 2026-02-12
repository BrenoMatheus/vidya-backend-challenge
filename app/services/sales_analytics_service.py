class SalesAnalyticsService:
    def __init__(self, repository):
        self.repository = repository

    def revenue_by_category(self):
        rows = self.repository.revenue_by_category()

        result = []
        for row in rows:
            average_ticket = (
                row.revenue / row.quantity if row.quantity > 0 else 0
            )

            result.append(
                {
                    "category": row.category,
                    "revenue": round(row.revenue, 2),
                    "quantity": row.quantity,
                    "average_ticket": round(average_ticket, 2),
                }
            )

        return result
