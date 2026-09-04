-- Hermes34 유지보수 고객 정규화 저장소 (PostgreSQL 14+)
-- DoWeb content_raw.contact[] 호환 JSON은 customer_contacts에서 생성한다.
-- password/token/private key 원문은 어떤 컬럼에도 저장하지 않는다.

BEGIN;

CREATE TABLE customers (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_content_idx UUID UNIQUE,
  name VARCHAR(200) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'inactive', 'lead', 'archived')),
  memo TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE customer_contacts (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  contact_type VARCHAR(30) NOT NULL
    CHECK (contact_type IN ('phone', 'email', 'kakao', 'other')),
  contact_name VARCHAR(100),
  contact_value VARCHAR(320) NOT NULL,
  is_primary BOOLEAN NOT NULL DEFAULT false,
  is_active BOOLEAN NOT NULL DEFAULT true,
  sort_order SMALLINT NOT NULL DEFAULT 0 CHECK (sort_order >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT customer_contacts_value_not_blank CHECK (btrim(contact_value) <> ''),
  CONSTRAINT customer_contacts_one_value_per_customer
    UNIQUE (customer_id, contact_type, contact_value)
);

CREATE UNIQUE INDEX customer_contacts_one_primary_per_customer
  ON customer_contacts (customer_id)
  WHERE is_primary AND is_active;
CREATE INDEX customer_contacts_customer_active_order
  ON customer_contacts (customer_id, is_active, sort_order, id);
CREATE INDEX customer_contacts_phone_lookup
  ON customer_contacts (contact_value)
  WHERE contact_type = 'phone' AND is_active;

CREATE TABLE categories (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  parent_id BIGINT REFERENCES categories(id) ON DELETE RESTRICT,
  name VARCHAR(100) NOT NULL,
  code VARCHAR(50) UNIQUE
);

CREATE TABLE members (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_member_idx UUID UNIQUE,
  name VARCHAR(100) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'inactive'))
);

CREATE TABLE projects (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_content_idx UUID UNIQUE,
  customer_id BIGINT NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  category_id BIGINT REFERENCES categories(id) ON DELETE SET NULL,
  title VARCHAR(250) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  memo TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX projects_customer_id ON projects (customer_id);

CREATE TABLE sites (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_content_idx UUID UNIQUE,
  project_id BIGINT NOT NULL REFERENCES projects(id) ON DELETE RESTRICT,
  primary_receiver_id BIGINT REFERENCES members(id) ON DELETE SET NULL,
  site_type VARCHAR(50) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  inspection_memo TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX sites_project_id ON sites (project_id);
CREATE INDEX sites_receiver_id ON sites (primary_receiver_id);

CREATE TABLE providers (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  provider_type VARCHAR(30) NOT NULL
    CHECK (provider_type IN ('domain_registrar', 'hosting', 'cloud', 'cdn', 'email', 'other')),
  name VARCHAR(200) NOT NULL,
  website VARCHAR(2048),
  UNIQUE (provider_type, name)
);

CREATE TABLE site_endpoints (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  site_id BIGINT NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
  provider_id BIGINT REFERENCES providers(id) ON DELETE SET NULL,
  endpoint_role VARCHAR(30) NOT NULL
    CHECK (endpoint_role IN ('public_domain', 'hosting_endpoint', 'admin_url', 'staging', 'other')),
  url VARCHAR(2048) NOT NULL,
  is_primary BOOLEAN NOT NULL DEFAULT false,
  CONSTRAINT site_endpoints_url_not_blank CHECK (btrim(url) <> ''),
  UNIQUE (site_id, endpoint_role, url)
);
CREATE UNIQUE INDEX site_endpoints_one_primary_per_role
  ON site_endpoints (site_id, endpoint_role)
  WHERE is_primary;

CREATE TABLE site_access_accounts (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  site_id BIGINT NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
  protocol VARCHAR(20) NOT NULL
    CHECK (protocol IN ('SSH', 'SFTP', 'FTP', 'CMS', 'DB')),
  auth_method VARCHAR(20) NOT NULL
    CHECK (auth_method IN ('password', 'ssh_key', 'oauth', 'token')),
  login_id VARCHAR(255),
  secret_ref VARCHAR(255) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'disabled', 'rotated')),
  UNIQUE (site_id, protocol, login_id)
);

CREATE TABLE site_notes (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  site_id BIGINT NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
  note_type VARCHAR(30) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMIT;
