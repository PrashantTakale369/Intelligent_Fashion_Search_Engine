-- Database schema for storing image metadata

CREATE TABLE IF NOT EXISTS fashion_images (
    image_id SERIAL PRIMARY KEY,
    image_path TEXT NOT NULL UNIQUE,
    normalized_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_image_path ON fashion_images(image_path);
CREATE INDEX IF NOT EXISTS idx_created_at ON fashion_images(created_at);
