#!/usr/bin/env node

/**
 * Node.js wrapper for the vectorizer library
 * Used by the Python API to call the native vectorizer
 */

const fs = require('fs');
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

    // Load the vectorizer module
    const vectorizerPath = path.join(__dirname, '..', 'index.js');
    const { vectorize, ColorMode, Hierarchical, PathSimplifyMode } = require(vectorizerPath);

    // Read input image
    const imageBuffer = fs.readFileSync(inputPath);

    // Build vectorizer options
    const options = {
      colorMode: config.colorMode === 'binary' ? ColorMode.Binary : ColorMode.Color,
      colorPrecision: config.colorPrecision || 8,
      filterSpeckle: config.filterSpeckle || 4,
      spliceThreshold: config.spliceThreshold || 45,
      cornerThreshold: config.cornerThreshold || 60,
      hierarchical: config.hierarchical === 'cutout' ? Hierarchical.Cutout : Hierarchical.Stacked,
      mode: config.mode === 'polygon' ? PathSimplifyMode.Polygon : 
            config.mode === 'none' ? PathSimplifyMode.None : PathSimplifyMode.Spline,
      layerDifference: config.layerDifference || 6,
      lengthThreshold: config.lengthThreshold || 4.0,
      maxIterations: config.maxIterations || 2,
      pathPrecision: config.pathPrecision || 5
    };

    // Convert to SVG
    const svg = await vectorize(imageBuffer, options);

    // Write output
    fs.writeFileSync(outputPath, svg, 'utf-8');

    console.log('SUCCESS');
    process.exit(0);
  } catch (error) {
    console.error('ERROR:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();
