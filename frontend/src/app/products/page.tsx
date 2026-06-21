"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Product } from "@/types";
import { Search, ShoppingCart, AlertCircle } from "lucide-react";
import toast from "react-hot-toast";
import Image from "next/image";

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timeout = setTimeout(() => {
      api.get(`/products/?search=${search}`).then(({ data }) => {
        setProducts(data.results || data);
        setLoading(false);
      });
    }, 400);
    return () => clearTimeout(timeout);
  }, [search]);

  const addToCart = async (productId: string) => {
    try {
      await api.post("/cart/", { product_id: productId, qty: 1 });
      toast.success("Added to cart");
    } catch {
      toast.error("Please log in to add items to cart.");
    }
  };

  return (
    <main className="max-w-6xl mx-auto py-8 px-4">
      <div className="flex items-center gap-3 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-400" />
          <input
            className="input pl-9"
            placeholder="Search medicines, vitamins..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="card animate-pulse h-48 bg-gray-100" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {products.map((product) => (
            <div key={product.id} className="card hover:shadow-md transition-shadow">
              <div className="relative w-full h-32 bg-gray-50 rounded-lg mb-3 overflow-hidden">
                {product.image ? (
                  <Image src={product.image} alt={product.name} fill className="object-contain" />
                ) : (
                  <div className="flex items-center justify-center h-full text-gray-300 text-4xl">💊</div>
                )}
              </div>
              {product.prescription_required && (
                <span className="inline-flex items-center gap-1 text-xs text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full mb-1">
                  <AlertCircle className="w-3 h-3" /> Rx
                </span>
              )}
              <h3 className="font-medium text-sm text-gray-900 line-clamp-2">{product.name}</h3>
              <p className="text-xs text-gray-400 mt-0.5">{product.generic_name}</p>
              <div className="flex items-center justify-between mt-3">
                <span className="font-bold text-green-700">SAR {product.price}</span>
                <button
                  onClick={() => addToCart(product.id)}
                  disabled={!product.in_stock}
                  className="p-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                >
                  <ShoppingCart className="w-4 h-4" />
                </button>
              </div>
              {!product.in_stock && (
                <p className="text-xs text-red-500 mt-1">Out of stock</p>
              )}
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
