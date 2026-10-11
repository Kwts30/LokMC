/**
 * LokMC — Cross-Platform Backend Runner
 * Automatically launches uvicorn using the project's virtual environment.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const rootDir = path.resolve(__dirname, '..');
const backendDir = path.join(rootDir, 'backend');
const isWin = process.platform === 'win32';

const venvPython = isWin
  ? path.join(backendDir, '.venv', 'Scripts', 'python.exe')
  : path.join(backendDir, '.venv', 'bin', 'python');

if (!fs.existsSync(venvPython)) {
  console.error('\x1b[31m[LokMC Error] Virtual environment Python not found at:\x1b[0m', venvPython);
  console.log('Initialize the environment with:');
  console.log('  py -m venv backend/.venv');
  console.log('  backend\\.venv\\Scripts\\pip install -r backend\\requirements.txt');
  process.exit(1);
}

const buildIndex = path.join(rootDir, 'frontend', 'build', 'index.html');
if (!fs.existsSync(buildIndex)) {
  console.log('\x1b[33m[LokMC] Building frontend assets (first-time build)...\x1b[0m');
  const { execSync } = require('child_process');
  execSync('npm run build', { cwd: path.join(rootDir, 'frontend'), stdio: 'inherit' });
}

console.log('\x1b[34m[LokMC]\x1b[0m Unified Server active on \x1b[32mhttp://localhost:8443\x1b[0m');
console.log('\x1b[90m  -> Web UI, API, and Server Orchestration on single port 8443\x1b[0m');

const proc = spawn(
  venvPython,
  ['-m', 'uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8443'],
  {
    cwd: backendDir,
    stdio: 'inherit',
    env: { ...process.env, PYTHONUNBUFFERED: '1' },
    shell: false,
  }
);

proc.on('close', (code) => {
  process.exit(code ?? 0);
});

proc.on('error', (err) => {
  console.error('\x1b[31m[LokMC Error] Failed to start backend:\x1b[0m', err.message);
  process.exit(1);
});
