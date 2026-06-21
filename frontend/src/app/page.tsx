"use client";
import Link from "next/link";
import { ShieldCheck, Brain, Truck, Users, ClipboardList, CreditCard } from "lucide-react";

const features = [
  { icon: ShieldCheck, title: "Verified Prescriptions", desc: "Upload prescriptions reviewed by licensed pharmacists." },
  { icon: Brain, title: "AI Health Assistant", desc: "Symptom checker with emergency detection and OTC recommendations." },
  { icon: Truck, title: "Fast Delivery", desc: "Home delivery with real-time tracking via WhatsApp." },
  { icon: Users, title: "Family Profiles", desc: "Manage medicines and reminders for your whole family." },
  { icon: ClipboardList, title: "Pharmacist Dashboard", desc: "Full counselling checklist and prescription verification." },
  { icon: CreditCard, title: "Secure Payments", desc: "Mada, Visa, Apple Pay, STC Pay, and Cash on Delivery." },
];

export default function HomePage() {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-green-600 to-teal-600 text-white py-24 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <ShieldCheck className="w-10 h-10" />
            <h1 className="text-4xl font-bold">Safe Pharmacy</h1>
          </div>
          <p className="text-xl text-green-100 mb-2">صيدلية آمنة</p>
          <p className="text-lg text-green-50 mb-8 max-w-2xl mx-auto">
            Saudi Arabia&apos;s trusted online pharmacy. Order medicines, consult pharmacists, and manage your family&apos;s health — all in one place.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link href="/products" className="bg-white text-green-700 font-semibold px-6 py-3 rounded-lg hover:bg-green-50 transition-colors">
              Browse Products
            </Link>
            <Link href="/ai-assistant" className="border-2 border-white text-white font-semibold px-6 py-3 rounded-lg hover:bg-white hover:text-green-700 transition-colors">
              AI Health Check
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4 max-w-6xl mx-auto">
        <h2 className="text-2xl font-bold text-center mb-12 text-gray-800">Why Safe Pharmacy?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f) => (
            <div key={f.title} className="card flex gap-4">
              <f.icon className="w-8 h-8 text-green-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-gray-900">{f.title}</h3>
                <p className="text-gray-500 text-sm mt-1">{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Prescription Notice */}
      <section className="bg-amber-50 border border-amber-200 rounded-xl mx-4 md:mx-auto max-w-2xl p-6 mb-16">
        <h3 className="font-semibold text-amber-800 mb-2">Prescription Medicine Notice</h3>
        <ul className="text-sm text-amber-700 space-y-1">
          <li>• Prescription medicine detected — please upload a valid prescription.</li>
          <li>• Keep the original prescription ready.</li>
          <li>• Hand the original to the delivery representative if required by pharmacy policy or applicable regulations.</li>
        </ul>
      </section>
    </main>
  );
}
