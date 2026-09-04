-- Apply only to databases created with 001_customer_maintenance_schema.sql
-- Project classification becomes searchable DoWeb-style tags; categories are not contents.

BEGIN;

ALTER TABLE projects DROP COLUMN category_id;
DROP TABLE categories;

ALTER TABLE projects
  ADD COLUMN tags TEXT NOT NULL DEFAULT '';
CREATE INDEX projects_tags_lookup ON projects USING GIN (string_to_array(tags, ' '));

ALTER TABLE sites
  DROP COLUMN site_type,
  ADD COLUMN site_type VARCHAR(30) NOT NULL DEFAULT 'other'
    CHECK (site_type IN ('production', 'development', 'staging', 'other')),
  ADD COLUMN tags TEXT NOT NULL DEFAULT '';
CREATE INDEX sites_tags_lookup ON sites USING GIN (string_to_array(tags, ' '));

COMMIT;