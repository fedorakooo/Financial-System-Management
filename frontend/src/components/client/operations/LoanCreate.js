import { useState } from "react";
import { useNavigate } from "react-router-dom";

const CreateLoan = () => {
  const navigate = useNavigate();
  const [loanData, setLoanData] = useState({
    amount: "",
    term_months: "",
    interest_rate: "",
    account: {
      bank_id: "",
      currency: "RUB",
    },
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name in loanData) {
      setLoanData({ ...loanData, [name]: value });
    } else if (name in loanData.account) {
      setLoanData({
        ...loanData,
        account: { ...loanData.account, [name]: value },
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "http://localhost:8000/profile/accounts/loan_accounts/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            loan_create_request: {
              amount: parseFloat(loanData.amount),
              term_months: parseInt(loanData.term_months),
              interest_rate: parseFloat(loanData.interest_rate),
            },
            account_create_request: {
              bank_id: loanData.account.bank_id,
              currency: "RUB",
            },
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка создания кредита");
      }

      const data = await response.json();
      alert("Кредит успешно создан!");
      navigate(`/loans/${data.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-6">Создание нового кредита</h1>
      
      {error && <p className="text-red-500 mb-4">{error}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Loan Information */}
        <div className="space-y-2">
          <h2 className="text-xl font-semibold">Информация о кредите</h2>
          
          <div>
            <label className="block text-gray-700 mb-1">Сумма кредита</label>
            <input
              type="number"
              step="0.01"
              min="1"
              name="amount"
              value={loanData.amount}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Введите сумму"
              required
            />
          </div>

          <div>
            <label className="block text-gray-700 mb-1">Срок (месяцев)</label>
            <select
              name="term_months"
              value={loanData.term_months}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-lg"
              required
            >
              <option value="">Выберите срок</option>
              <option value="3">3 месяца</option>
              <option value="6">6 месяцев</option>
              <option value="12">12 месяцев</option>
              <option value="24">24 месяца</option>
              <option value="36">36 месяцев</option>
              <option value="48">48 месяцев</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-700 mb-1">Процентная ставка</label>
            <input
              type="number"
              step="0.01"
              min="0.1"
              name="interest_rate"
              value={loanData.interest_rate}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Введите процентную ставку"
              required
            />
          </div>
        </div>

        {/* Account Information */}
        <div className="space-y-2">
          <h2 className="text-xl font-semibold">Информация о счёте</h2>
          
          <div>
            <label className="block text-gray-700 mb-1">ID банка</label>
            <input
              type="text"
              name="bank_id"
              value={loanData.account.bank_id}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Введите ID банка"
              required
            />
          </div>
        </div>

        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
            disabled={loading}
          >
            Отмена
          </button>
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:bg-blue-300"
            disabled={loading}
          >
            {loading ? "Создание..." : "Создать кредит"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateLoan;