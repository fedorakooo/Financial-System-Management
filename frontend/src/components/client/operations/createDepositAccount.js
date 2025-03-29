import { useState } from "react";
import { useNavigate } from "react-router-dom";

const CreateDepositAccount = () => {
  const [amount, setAmount] = useState("");
  const [interestRate, setInterestRate] = useState("");
  const [fromAccountId, setFromAccountId] = useState("");
  const [bankId, setBankId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    const token = localStorage.getItem("access_token");
    const depositData = {
      amount: parseFloat(amount),
      interest_rate: parseFloat(interestRate),
      from_account_id: parseInt(fromAccountId),
    };

    const accountData = {
      bank_id: parseInt(bankId),
    };
    
    try {
      const response = await fetch("http://localhost:8000/profile/accounts/deposit_accounts/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          deposit_create_request: depositData,
          account_create_request: accountData,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка при создании счета");
      }

      const data = await response.json();
      navigate(`/deposit_accounts/${data.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold">Создать депозитный счет</h1>
      {error && <p style={{ color: "red" }}>Ошибка: {error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block">Сумма</label>
          <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} className="border p-2 w-full" required />
        </div>
        <div>
          <label className="block">Процентная ставка</label>
          <input type="number" step="0.01" value={interestRate} onChange={(e) => setInterestRate(e.target.value)} className="border p-2 w-full" required />
        </div>
        <div>
          <label className="block">Исходный счет ID</label>
          <input type="number" value={fromAccountId} onChange={(e) => setFromAccountId(e.target.value)} className="border p-2 w-full" required />
        </div>
        <div>
          <label className="block">Банк ID</label>
          <input type="number" value={bankId} onChange={(e) => setBankId(e.target.value)} className="border p-2 w-full" required />
        </div>
        <button type="submit" className="bg-blue-500 text-white p-2 rounded" disabled={loading}>
          {loading ? "Создание..." : "Создать"}
        </button>
      </form>
    </div>
  );
};

export default CreateDepositAccount;