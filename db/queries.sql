-- To comment / uncomment_
-- to uncomment and press ⌘ / (Cmd + forward slash

-- =============================================
-- Amalgamator – News Sources Table Queries
-- =============================================
-- Usage:
--   cd /Users/SimonsMBA/Documents/DevOps/amalgamator_project
--   Run entire file:   sqlite3 -header -column amalgamator.db < db/queries.sql
--   Interactive mode:   sqlite3 -header -column amalgamator.db
--                       .read db/queries.sql
--   Single query:       sqlite3 -header -column amalgamator.db "SELECT ..."
--

-- Tip: Comment/uncomment the queries you need.
-- =============================================

-- 0. List all tables in the database
SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name;

-- 1. All sources (ordered by active → name)
-- SELECT id, source_name, section, source_type, active
-- FROM news_sources
-- ORDER BY active DESC, source_name;

-- 2. Active sources only
-- SELECT id, source_name, section, source_type, url
-- FROM news_sources
-- WHERE active = 1
-- ORDER BY source_name;

-- 3. Inactive sources only
-- SELECT id, source_name, section, source_type, url
-- FROM news_sources
-- WHERE active = 0
-- ORDER BY source_name;

-- 4. Count sources by status
-- SELECT
--     CASE active WHEN 1 THEN 'Active' ELSE 'Inactive' END AS status,
--     COUNT(*) AS total
-- FROM news_sources
-- GROUP BY active;

-- 5. Count sources by source type
-- SELECT source_type, COUNT(*) AS total
-- FROM news_sources
-- GROUP BY source_type;

-- 6. Count sources by name
-- SELECT source_name, COUNT(*) AS feeds
-- FROM news_sources
-- GROUP BY source_name
-- ORDER BY feeds DESC;

-- 7. Search by name (change the LIKE pattern)
-- SELECT id, source_name, section, source_type, active
-- FROM news_sources
-- WHERE source_name LIKE '%BBC%';

-- 8. Search by section
-- SELECT id, source_name, section, source_type, active
-- FROM news_sources
-- WHERE section LIKE '%Tech%';

-- =============================================
-- WRITE OPERATIONS (uncomment to use)
-- =============================================

-- 9. Activate a source by id
-- UPDATE news_sources SET active = 1 WHERE id = 10;

-- 10. Deactivate a source by id
-- UPDATE news_sources SET active = 0 WHERE id = 4;

-- 11. Activate all sources for a given name
-- UPDATE news_sources SET active = 1 WHERE source_name = 'BBC News';

-- 12. Add a new source
-- INSERT INTO news_sources (source_name, section, source_type, url, active)
-- VALUES ('Reuters', 'World', 'rss', 'https://feeds.reuters.com/reuters/worldNews', 1);

-- 13. Delete a source by id
-- DELETE FROM news_sources WHERE id = 99;

-- 14. Show full row detail for one source
-- SELECT * FROM news_sources WHERE id = 1;


-- =============================================================
-- NEWS ARTICLES TABLE
-- =============================================================

-- 15. Recent articles (last 20)
-- SELECT id, date_added, source, section_name, headline
-- FROM news_articles
-- ORDER BY id DESC
-- LIMIT 20;

-- 16. All articles from a specific source
-- SELECT id, date_added, section_name, headline, web_url
-- FROM news_articles
-- WHERE source = 'BBC News'
-- ORDER BY id DESC;

-- 17. Count articles per source
-- SELECT source, COUNT(*) AS total
-- FROM news_articles
-- GROUP BY source
-- ORDER BY total DESC;

-- 18. Count articles per section
-- SELECT section_name, COUNT(*) AS total
-- FROM news_articles
-- GROUP BY section_name
-- ORDER BY total DESC;

-- 19. Search articles by headline keyword
-- SELECT id, source, headline, web_url
-- FROM news_articles
-- WHERE headline LIKE '%climate%';

-- 20. Articles added today
-- SELECT id, date_added, source, headline
-- FROM news_articles
-- WHERE date_added >= date('now')
-- ORDER BY id DESC;

-- 21. Total article count
-- SELECT COUNT(*) AS total_articles FROM news_articles;

-- 22. Delete all articles from a specific source
-- DELETE FROM news_articles WHERE source = 'Associated Press';


-- =============================================================
-- USERS TABLE
-- =============================================================

-- 23. All users
-- SELECT id, first_name, last_name, email, tier, timezone, delivery_schedule, active
-- FROM users
-- ORDER BY last_name, first_name;

-- 24. Active users only
-- SELECT id, first_name, last_name, email, tier, timezone, delivery_schedule
-- FROM users
-- WHERE active = 1;

-- 25. Add a new user
-- INSERT INTO users (email, first_name, last_name, tier, timezone, delivery_schedule, active)
-- VALUES ('jane@example.com', 'Jane', 'Doe', 1, 'America/New_York', 'hourly', 1);

-- 26. Deactivate a user
-- UPDATE users SET active = 0 WHERE id = 2;


-- =============================================================
-- USER SUBSCRIPTIONS TABLE
-- =============================================================

-- 27. Show all subscriptions with user and source names
-- SELECT us.id, u.first_name, u.last_name, u.email, s.source_name, s.section
-- FROM user_subscriptions us
-- JOIN users u ON u.id = us.user_id
-- JOIN news_sources s ON s.id = us.source_id
-- ORDER BY u.last_name, s.source_name;

-- 28. Subscriptions for a specific user
-- SELECT s.source_name, s.section, s.source_type, us.subscribed_at
-- FROM user_subscriptions us
-- JOIN news_sources s ON s.id = us.source_id
-- WHERE us.user_id = 1
-- ORDER BY s.source_name;

-- 29. Subscribe a user to a source
-- INSERT INTO user_subscriptions (user_id, source_id) VALUES (1, 10);

-- 30. Unsubscribe a user from a source
-- DELETE FROM user_subscriptions WHERE user_id = 1 AND source_id = 10;

-- 31. Count subscriptions per user
-- SELECT u.first_name, u.last_name, COUNT(*) AS subscriptions
-- FROM user_subscriptions us
-- JOIN users u ON u.id = us.user_id
-- GROUP BY u.first_name, u.last_name
-- ORDER BY subscriptions DESC;


-- =============================================================
-- USER DELIVERIES TABLE
-- =============================================================

-- 32. Recent deliveries (last 20)
-- SELECT ud.id, u.first_name, u.last_name, a.source, a.headline, ud.delivered_at
-- FROM user_deliveries ud
-- JOIN users u ON u.id = ud.user_id
-- JOIN news_articles a ON a.id = ud.article_id
-- ORDER BY ud.id DESC
-- LIMIT 20;

-- 33. Count deliveries per user
-- SELECT u.first_name, u.last_name, COUNT(*) AS delivered
-- FROM user_deliveries ud
-- JOIN users u ON u.id = ud.user_id
-- GROUP BY u.first_name, u.last_name;

-- 34. Pending articles for a user (not yet delivered)
-- SELECT a.id, a.source, a.headline, a.last_modified
-- FROM news_articles a
-- JOIN news_sources s ON a.source = s.source_name
-- JOIN user_subscriptions us ON us.source_id = s.id AND us.user_id = 1
-- WHERE a.id NOT IN (
--     SELECT article_id FROM user_deliveries WHERE user_id = 1
-- )
-- ORDER BY a.id DESC;

-- 35. Clear delivery history for a user (re-send everything)
-- DELETE FROM user_deliveries WHERE user_id = 1;


-- =============================================================
-- USER TIER CHANGES TABLE
-- =============================================================

-- 36. All tier changes (most recent first)
-- SELECT tc.id, u.first_name, u.last_name, tc.prev_tier, tc.new_tier, tc.date_of_change
-- FROM user_tier_changes tc
-- JOIN users u ON u.id = tc.user_id
-- ORDER BY tc.date_of_change DESC;

-- 37. Tier history for a specific user
-- SELECT prev_tier, new_tier, date_of_change
-- FROM user_tier_changes
-- WHERE user_id = 1
-- ORDER BY date_of_change DESC;

-- 38. Upgrade a user to tier 2 (run both statements together)
-- UPDATE users SET tier = 2 WHERE id = 1;
-- INSERT INTO user_tier_changes (user_id, prev_tier, new_tier)
-- VALUES (1, 1, 2);

-- 39. Downgrade a user back to tier 1
-- UPDATE users SET tier = 1 WHERE id = 1;
-- INSERT INTO user_tier_changes (user_id, prev_tier, new_tier)
-- VALUES (1, 2, 1);

-- 40. Count users per tier
-- SELECT tier, COUNT(*) AS total FROM users GROUP BY tier;


-- =============================================================
-- USER PAYMENTS TABLE
-- =============================================================

-- 41. All payments (most recent first)
-- SELECT p.id, u.first_name, u.last_name, p.payment_amount, p.payment_currency,
--        p.service_provider, p.payment_type, p.payment_date
-- FROM user_payments p
-- JOIN users u ON u.id = p.user_id
-- ORDER BY p.payment_date DESC;

-- 42. Payments for a specific user
-- SELECT payment_amount, payment_currency, service_provider, payment_type, payment_date
-- FROM user_payments
-- WHERE user_id = 1
-- ORDER BY payment_date DESC;

-- 43. Total revenue by currency
-- SELECT payment_currency, SUM(CAST(payment_amount AS REAL)) AS total_revenue, COUNT(*) AS payments
-- FROM user_payments
-- GROUP BY payment_currency;

-- 44. Revenue by provider
-- SELECT service_provider, COUNT(*) AS payments, SUM(CAST(payment_amount AS REAL)) AS total
-- FROM user_payments
-- GROUP BY service_provider;

-- 45. Record a payment
-- INSERT INTO user_payments (user_id, payment_amount, payment_currency, service_provider, payment_type)
-- VALUES (1, '2.99', 'EUR', 'stripe', 'subscription');


-- =============================================================
-- LOOKUP TIERS TABLE
-- =============================================================

-- 46. All tiers
-- SELECT id, tier_name, date_added FROM lookup_tiers ORDER BY id;

-- 47. Add a new tier
-- INSERT INTO lookup_tiers (id, tier_name) VALUES (3, 'enterprise');

-- 48. Users with tier names (join)
-- SELECT u.id, u.first_name, u.last_name, u.email, lt.tier_name, u.active
-- FROM users u
-- JOIN lookup_tiers lt ON lt.id = u.tier
-- ORDER BY u.last_name;
