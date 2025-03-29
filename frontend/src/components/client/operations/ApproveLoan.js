import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const ApproveLoan = () => {
  const { loan_account_id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [loanDetails, setLoanDetails] = useState(null);

  const handleApprove = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `http://localhost:8000/loans/${loan_account_id}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка при одобрении кредита");
      }

      const data = await response.json();
      setLoanDetails(data);
      setSuccess(true);
      alert("Кредит успешно одобрен!");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-semibold mb-6">Одобрение кредита #{loan_account_id}</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {success ? (
        <div className="space-y-4">
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            Кредит успешно одобрен!
          </div>

          <div className="bg-white shadow rounded-lg p-4">
            <h2 className="text-xl font-semibold mb-4">Детали кредита</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h3 className="font-medium text-gray-700">Информация о кредите</h3>
                <p className="mt-1">
                  <span className="font-medium">Сумма:</span> {loanDetails.loan.amount} RUB
                </p>
                <p>
                  <span className="font-medium">Срок:</span> {loanDetails.loan.term_months} месяцев
                </p>
                <p>
                  <span className="font-medium">Процентная ставка:</span> {loanDetails.loan.interest_rate}%
                </p>
              </div>

              <div>
                <h3 className="font-medium text-gray-700">Информация о счёте</h3>
                <p className="mt-1">
                  <span className="font-medium">ID счёта:</span> {loanDetails.account.id}
                </p>
                <p>
                  <span className="font-medium">ID банка:</span> {loanDetails.account.bank_id}
                </p>
                <p>
                  <span className="font-medium">Валюта:</span> {loanDetails.account.currency}
                </p>
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              onClick={() => navigate("/loans")}
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
            >
              Вернуться к списку кредитов
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-white shadow rounded-lg p-6">
          <div className="mb-6">
            <p className="text-gray-700">
              Вы уверены, что хотите одобрить этот кредит? После одобрения будут созданы 
              соответствующие записи и клиент получит уведомление.
            </p>
          </div>

          <div className="flex justify-end gap-4">
            <button
              onClick={() => navigate(-1)}
              className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
            >
              Отмена
            </button>
            <button
              onClick={handleApprove}
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
            >
              Одобрить кредит
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ApproveLoan;