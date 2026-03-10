import mysql from 'mysql2/promise';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function initDB() {
    console.log('Reading create_tables.sql...');
    const sqlPath = path.join(__dirname, 'create_tables.sql');
    const sql = fs.readFileSync(sqlPath, 'utf8');

    // Split SQL into individual statements
    // This is a simple split, might need refinement for complex SQL but should work for standard schema files
    const statements = sql
        .split(/;(?:\s|$)/)
        .map(s => s.trim())
        .filter(s => s.length > 0 && !s.startsWith('--'));

    console.log(`Found ${statements.length} SQL statements.`);

    try {
        const connection = await mysql.createConnection({
            host: 'localhost',
            user: 'root',
            password: 'Dh10062006@10',
            database: 'rental_system',
            multipleStatements: true // Allow multi-statement execution
        });

        console.log('✓ Connected to MySQL');

        // We can execute the whole thing at once if multipleStatements is true
        await connection.query(sql);
        console.log('✓ Successfully executed all SQL statements');

        const [rows] = await connection.execute('SHOW TABLES');
        console.log('Total tables now:', rows.length);

        await connection.end();
    } catch (err) {
        console.error('✗ Failed to initialize database:', err.message);
    }
}

initDB();
