#!/usr/bin/env node

/**
 * Node.js wrapper for the vectorizer CLI
 * Used by the Python API to call the vectorizer
 */

const { spawn } = require('child_process');
const path = require('path');

async function main() {
  try {
    // Read arguments from command line
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
      console.error('Usage: node vectorizer_wrapper.js <input.png> <output.svg> [config_json]');
      process.exit(1);
    }

    const inputPath = args[0];
    const outputPath = args[1];
    const configJson = args[2] || '{}';

    // Parse configuration
    const config = JSON.parse(configJson);

    // Build CLI arguments
    const cliArgs = [inputPath, outputPath];
    
    if (config.colorMode === 'binary') {
      cliArgs.push('--color-mode', 'binary');
    } else {
      cliArgs.push('--color-mode', 'color');
    }
    
    if (config.colorPrecision) cliArgs.push('--color-precision', config.colorPrecision.toString());
    if (config.filterSpeckle) cliArgs.push('--filter-speckle', config.filterSpeckle.toString());
    if (config.spliceThreshold) cliArgs.push('--splice-threshold', config.spliceThreshold.toString());
    if (config.cornerThreshold) cliArgs.push('--corner-threshold', config.cornerThreshold.toString());
    if (config.layerDifference) cliArgs.push('--layer-difference', config.layerDifference.toString());
    if (config.lengthThreshold) cliArgs.push('--length-threshold', config.lengthThreshold.toString());
    if (config.maxIterations) cliArgs.push('--max-iterations', config.maxIterations.toString());
    if (config.pathPrecision) cliArgs.push('--path-precision', config.pathPrecision.toString());
    
    if (config.hierarchical === 'cutout') {
      cliArgs.push('--hierarchical', 'cutout');
    } else {
      cliArgs.push('--hierarchical', 'stacked');
    }
    
    if (config.mode === 'polygon') {
      cliArgs.push('--mode', 'polygon');
    } else if (config.mode === 'none') {
      cliArgs.push('--mode', 'none');
    } else {
      cliArgs.push('--mode', 'spline');
    }

    // Get CLI path
    const cliPath = path.join(__dirname, '..', 'cli', 'index.mjs');

    // Run CLI
    const child = spawn('node', [cliPath, ...cliArgs], {
      stdio: ['ignore', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    child.on('close', (code) => {
      if (code === 0) {
        console.log('SUCCESS');
        process.exit(0);
      } else {
        console.error('ERROR:', stderr || stdout);
        process.exit(1);
      }
    });

  } catch (error) {
    console.error('ERROR:', error.message);
    process.exit(1);
  }
}

main();
