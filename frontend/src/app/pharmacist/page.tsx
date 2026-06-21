"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { ClipboardList, MessageCircle, Truck, FileText, CheckCircle, XCircle } from "lucide-react";

interface DashboardStats {
  pending_orders: number;
  prescription_orders: number;
  open_chats: number;
  active_deliveries: number;
}

interface Order {
  id: string;
  order_number: string;
  status: string;
  total: string;
  created_at: string;
  user?: { name: string; mobile: string };
}

export default function PharmacistDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [activeTab, setActiveTab] = useState<"pending" | "prescriptions" | "chats">("pending");

  useEffect(() => {
    api.get("/pharmacist/dashboard/").then(({ data }) => setStats(data));
    api.get("/pharmacist/orders/?status=pending").then(({ data }) =>
      setOrders(data.results || data)
    );
  }, []);

  const statCards = stats
    ? [
        { label: "Pending Orders", value: stats.pending_orders, icon: ClipboardList, color: "text-blue-600 bg-blue-50" },
        { label: "Prescription Orders", value: stats.prescription_orders, icon: FileText, color: "text-amber-600 bg-amber-50" },
        { label: "Open Chats", value: stats.open_chats, icon: MessageCircle, color: "text-green-600 bg-green-50" },
        { label: "Active Deliveries", value: stats.active_deliveries, icon: Truck, color: "text-purple-600 bg-purple-50" },
      ]
    : [];

  return (
    <main className="max-w-6xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">Pharmacist Dashboard</h1>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {statCards.map((s) => (
          <div key={s.label} className="card">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center mb-3 ${s.color}`}>
              <s.icon className="w-5 h-5" />
            </div>
            <p className="text-2xl font-bold text-gray-900">{s.value}</p>
            <p className="text-sm text-gray-500">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Orders Table */}
      <div className="card">
        <h2 className="font-semibold text-gray-800 mb-4">Pending Orders</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-gray-500">
                <th className="text-left py-2 font-medium">Order #</th>
                <th className="text-left py-2 font-medium">Status</th>
                <th className="text-left py-2 font-medium">Total</th>
                <th className="text-left py-2 font-medium">Date</th>
                <th className="text-left py-2 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id} className="border-b last:border-0 hover:bg-gray-50">
                  <td className="py-3 font-medium text-green-700">{order.order_number}</td>
                  <td className="py-3">
                    <span className="px-2 py-0.5 bg-yellow-100 text-yellow-700 rounded-full text-xs capitalize">
                      {order.status}
                    </span>
                  </td>
                  <td className="py-3">SAR {order.total}</td>
                  <td className="py-3 text-gray-400">{new Date(order.created_at).toLocaleDateString()}</td>
                  <td className="py-3">
                    <div className="flex gap-2">
                      <button className="p-1 text-green-600 hover:bg-green-50 rounded">
                        <CheckCircle className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-red-500 hover:bg-red-50 rounded">
                        <XCircle className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Counselling Checklist info */}
      <div className="card mt-4 bg-green-50 border-green-200">
        <h3 className="font-semibold text-green-800 mb-2">Counselling Checklist</h3>
        <ul className="text-sm text-green-700 space-y-1">
          {["Indication explained", "Dose explained", "Duration explained", "Storage explained", "Side effects explained"].map((item) => (
            <li key={item} className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4" /> {item}
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
