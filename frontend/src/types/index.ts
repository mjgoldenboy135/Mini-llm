export interface User {
  id: string;
  mobile: string;
  name: string;
  email: string;
  role: "customer" | "pharmacist" | "delivery" | "admin";
  date_joined: string;
  avatar: string | null;
}

export interface Product {
  id: string;
  sku: string;
  name: string;
  name_ar: string;
  generic_name: string;
  brand: string;
  category: string;
  category_name: string;
  price: string;
  stock: number;
  image: string | null;
  prescription_required: boolean;
  in_stock: boolean;
  dosage_form: string;
  strength: string;
}

export interface CartItem {
  id: string;
  product: Product;
  qty: number;
  line_total: string;
}

export interface Cart {
  id: string;
  items: CartItem[];
  total: string;
  item_count: number;
  has_prescription_items: boolean;
}

export interface OrderItem {
  id: string;
  product: Product;
  qty: number;
  price: string;
  line_total: string;
}

export interface Order {
  id: string;
  order_number: string;
  status: string;
  payment_method: string;
  delivery_type: string;
  subtotal: string;
  delivery_fee: string;
  total: string;
  items: OrderItem[];
  created_at: string;
}

export interface FamilyMember {
  id: string;
  name: string;
  relationship: string;
  dob: string;
  gender: string;
  allergies: string;
  medical_conditions: string;
  current_medicines: string;
}

export interface AISessionResponse {
  session_id: string;
  symptom: string;
  is_emergency: boolean;
  questions?: Array<{
    step: number;
    question: string;
    options: string[];
    multi?: boolean;
  }>;
  title?: string;
  message?: string;
  advice?: string;
  disclaimer?: string;
  recommended_products?: Product[];
}
