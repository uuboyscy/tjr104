## Client Background

Company XXX runs stores in many countries and also sells online. The leadership team wants one simple way to collect `web events` and `in-store sales` so the new CRM can launch campaigns without waiting for manual reports.

## Data Sources

- **Web analytics**: Website tracking shows every logged-in action (page views, wishlist events, cart moves, orders, hashed emails, etc.) and is reachable through a `REST API`.

- **In-store sales data**: Daily flat files from the store systems list customer contact info, products bought, prices, discounts, and purchase times.

*Assume store staff capture personal data such as email addresses during checkout.*

## Data Destination

- **CRM**: The CRM system must store full customer profiles for both `store` and `web shoppers`, plus reusable marketing segments (example: people who spent more than $500 in the past 14 days). Teams can push data through the `CRM API` to create, update, or delete profiles and segments.

## Requirements

### Business

- Segments in the CRM need to `refresh every` day so email and SMS workflows always use the latest data.
- Segments include both `simple rules` (for example, someone who bought an item over $500 in-store last week after browsing online three days earlier) and `ML results`.
- Only a few ML models exist and they are retrained `twice a year`.
- Rule-based segments change often, and new requests may arrive `weekly` once the system goes live.

### Technical

- Pick Azure, AWS, or GCP when presenting your design.
- The Data Science team will hand over notebooks that contain the ML logic.

## Your Goal

You will have a workshop with the client `CMO`, `CDO`, and `Head of Security`. Use this session to:

1. Give a high-level view of the cloud and data architecture.
2. Outline a simple staffing view, noting key roles and rough mandays.
