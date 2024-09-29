import React, { useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const LeafAnalysis = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await axios.post('http://localhost:5000/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error analyzing leaf:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderChart = (data, title) => {
    const chartData = Object.entries(data).map(([name, value]) => ({ name, value }));
    return (
      <div className="mb-4">
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        <LineChart width={400} height={200} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="value" stroke="#8884d8" />
        </LineChart>
      </div>
    );
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Leaf Image Analysis</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <input type="file" onChange={handleFileChange} className="mb-2" />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded" disabled={!file || loading}>
          {loading ? 'Analyzing...' : 'Analyze Leaf'}
        </button>
      </form>

      {results && (
        <div>
          <h2 className="text-xl font-semibold mb-3">Analysis Results</h2>
          {renderChart(results.disease_detection, 'Disease Detection')}
          {renderChart(results.pest_damage, 'Pest Damage')}
          {renderChart(results.leaf_morphology, 'Leaf Morphology')}
          {renderChart({ chlorophyll: results.chlorophyll_content }, 'Chlorophyll Content')}
          {renderChart(results.species_identification, 'Species Identification')}
        </div>
      )}
    </div>
  );
};

export default LeafAnalysis;