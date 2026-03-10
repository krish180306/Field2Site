// Run migration: add Password column to HOST and BUYER tables
import mysql from 'mysql2/promise';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';
const require = createRequire(import.meta.url);
const dotenv = require('dotenv');

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
dotenv.config({ path: path.join(__dirname, 'server', '.env') });

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'rental_system',
});

async function runMigration() {
    const conn = await pool.getConnection();
    try {
        console.log('🔄 Running password migration...');

        // Check if Password column already exists in HOST
        const [hostCols] = await conn.execute(`
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'HOST' AND COLUMN_NAME = 'Password'
        `);
        if (hostCols.length === 0) {
            await conn.execute(`ALTER TABLE HOST ADD COLUMN Password VARCHAR(255) NOT NULL DEFAULT 'field2site123'`);
            console.log('✓ Added Password column to HOST');
        } else {
            console.log('ℹ  Password column already exists in HOST — skipping ALTER');
        }

        // Check if Password column already exists in BUYER
        const [buyerCols] = await conn.execute(`
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'BUYER' AND COLUMN_NAME = 'Password'
        `);
        if (buyerCols.length === 0) {
            await conn.execute(`ALTER TABLE BUYER ADD COLUMN Password VARCHAR(255) NOT NULL DEFAULT 'field2site123'`);
            console.log('✓ Added Password column to BUYER');
        } else {
            console.log('ℹ  Password column already exists in BUYER — skipping ALTER');
        }

        // Set default password for all existing users
        const [hostUpdate] = await conn.execute(`UPDATE HOST SET Password = 'field2site123' WHERE Password IS NULL OR Password = '' OR Password = 'field2site123'`);
        console.log(`✓ Set default password for ${hostUpdate.affectedRows} HOST rows`);

        const [buyerUpdate] = await conn.execute(`UPDATE BUYER SET Password = 'field2site123' WHERE Password IS NULL OR Password = '' OR Password = 'field2site123'`);
        console.log(`✓ Set default password for ${buyerUpdate.affectedRows} BUYER rows`);

        // Confirm
        const [hosts] = await conn.execute('SELECT Host_ID, Host_Name, Email, Password FROM HOST');
        const [buyers] = await conn.execute('SELECT Buyer_ID, Name, Email, Password FROM BUYER');

        console.log('\n📋 HOST users:');
        hosts.forEach(h => console.log(`  [ID:${h.Host_ID}] ${h.Host_Name} <${h.Email}> → password: ${h.Password}`));

        console.log('\n📋 BUYER users:');
        buyers.forEach(b => console.log(`  [ID:${b.Buyer_ID}] ${b.Name} <${b.Email}> → password: ${b.Password}`));

        console.log('\n✅ Migration complete!');
    } catch (err) {
        console.error('❌ Migration failed:', err.message);
    } finally {
        conn.release();
        await pool.end();
    }
}

runMigration();
