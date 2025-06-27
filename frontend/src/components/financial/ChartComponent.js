import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Jan', income: 4000, expenses: 2400, savings: 1600 },
  { name: 'Feb', income: 3000, expenses: 1398, savings: 1602 },
  { name: 'Mar', income: 5000, expenses: 3800, savings: 1200 },
  { name: 'Apr', income: 4780, expenses: 3908, savings: 872 },
  { name: 'May', income: 5890, expenses: 4800, savings: 1090 },
  { name: 'Jun', income: 4390, expenses: 3800, savings: 590 },
  { name: 'Jul', income: 4000, expenses: 4300, savings: -300 },
];

const ChartComponent = ({ title = "Financial Overview" }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="income" stroke="#8884d8" activeDot={{ r: 8 }} />
          <Line type="monotone" dataKey="expenses" stroke="#82ca9d" />
          <Line type="monotone" dataKey="savings" stroke="#ffc658" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartComponent;