"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

export default function Home() {

  const [totalCost, setTotalCost] = useState(0);
  const [totalTokens, setTotalTokens] = useState(0);
  const [topFeatures, setTopFeatures] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [roiData, setRoiData] = useState([]);

  useEffect(() => {

    fetchAnalytics();

  }, []);

  const fetchAnalytics = async () => {

    try {

      const costRes = await axios.get(
        "http://127.0.0.1:8000/analytics/total-cost"
      );

      const tokenRes = await axios.get(
        "http://127.0.0.1:8000/analytics/total-tokens"
      );

      const featureRes = await axios.get(
        "http://127.0.0.1:8000/analytics/top-features"
      );
      const chartRes = await axios.get(
        "http://127.0.0.1:8000/analytics/cost-by-feature"
      );
      const roiRes = await axios.get(
        "http://127.0.0.1:8000/analytics/roi-by-feature"
      );

      setRoiData(roiRes.data);
      setChartData(chartRes.data);
      setTotalCost(costRes.data.total_ai_cost);
      setTotalTokens(tokenRes.data.total_tokens);
      setTopFeatures(featureRes.data);

    } catch (error) {

      console.error(error);

    }

  };

  return (

    <main className="min-h-screen bg-black text-white p-10">

      <h1 className="text-5xl font-bold mb-12 tracking-tight">
        AI ROI Tracker Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <div className="
    border border-zinc-800
    bg-zinc-950
    p-8
    rounded-2xl
    hover:border-purple-500
    transition
  ">

          <h2 className="text-zinc-400 text-lg">
            Total AI Cost
          </h2>

          <p className="text-5xl font-bold mt-6">
            ${totalCost.toFixed(6)}
          </p>

        </div>

        <div className="
    border border-zinc-800
    bg-zinc-950
    p-8
    rounded-2xl
    hover:border-blue-500
    transition
  ">

          <h2 className="text-zinc-400 text-lg">
            Total Tokens
          </h2>

          <p className="text-5xl font-bold mt-6">
            {totalTokens}
          </p>

        </div>

      </div>

      <div className="
  mt-10
  border border-zinc-800
  bg-zinc-950
  p-8
  rounded-2xl
">

        <h2 className="text-2xl font-bold mb-4">
          Top Features
        </h2>

        {topFeatures.map((feature: any, index: number) => (

          <div
            key={index}
            className="
  flex justify-between
  border-b border-zinc-800
  py-4
  hover:bg-zinc-900
  px-2
  rounded-lg
  transition
">

            <span>{feature.feature_name}</span>

            <span>${feature.total_cost.toFixed(6)}</span>

          </div>

        ))}
        <div className="mt-10 border border-zinc-800 bg-zinc-950 p-8 rounded-2xl">

          <h2 className="text-2xl font-bold mb-6">
            Cost By Feature
          </h2>

          <div className="h-100">

            <ResponsiveContainer width="100%" height="100%">

              <BarChart data={chartData}>

                <XAxis dataKey="feature_name" />

                <YAxis />

                <Tooltip
                  contentStyle={{
                    backgroundColor: "#18181b",
                    border: "1px solid #27272a",
                    borderRadius: "10px"
                  }}
                />

                <Bar
                  dataKey="total_cost"
                  fill="#7c3aed"
                  radius={[10, 10, 0, 0]}
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>
      <div className="
  mt-10
  border border-zinc-800
  bg-zinc-950
  p-8
  rounded-2xl
">

        <h2 className="text-2xl font-bold mb-6">
          ROI By Feature
        </h2>

        <div className="h-[400px]">

          <ResponsiveContainer width="100%" height="100%">

            <BarChart data={roiData}>

              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />

              <XAxis dataKey="feature_name" />

              <YAxis />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#18181b",
                  border: "1px solid #27272a",
                  borderRadius: "10px"
                }}
              />

              <Bar
                dataKey="avg_roi"
                fill="#22c55e"
                radius={[10, 10, 0, 0]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

    </main>
  );
}