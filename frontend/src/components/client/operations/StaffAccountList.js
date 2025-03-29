import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

const AccountList = () => {
  const [searchParams] = useSearchParams();
  const user_id = searchParams.get("user_id");
  const navigate = useNavigate();
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const token = localStorage.getItem('access_token');
        const numericUserId = parseInt(user_id, 10);
      
        if (isNaN(numericUserId) || numericUserId <= 0) {
          throw new Error('ID пользователя должен быть положительным числом');
        }

        const response = await fetch(
          `http://localhost:8000/staff/accounts/?user_id=${numericUserId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Не удалось загрузить счета');
        }

        const data = await response.json();
        setAccounts(data);
      } catch (err) {
        setError(err.message);
        console.error('Ошибка при загрузке счетов:', err);
      } finally {
        setLoading(false);
      }
    };

    if (user_id) {
      fetchAccounts();
    }
  }, [user_id]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'ACTIVE': return 'bg-green-100 text-green-800';
      case 'BLOCKED': return 'bg-red-100 text-red-800';
      case 'FROZEN': return 'bg-blue-100 text-blue-800';
      case 'ON_CONSIDERATION': return 'bg-yellow-100 text-yellow-800';
      case 'CANCELLED': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeText = (type) => {
    switch (type) {
      case 'SALARY': return 'Зарплатный';
      case 'DEPOSIT': return 'Депозитный';
      case 'SETTLEMENT': return 'Расчётный';
      case 'LOAN': return 'Кредитный';
      case 'ENTERPRISE': return 'Корпоративный';
      default: return type;
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user_id) {
    return (
      <div className="p-4 max-w-4xl mx-auto">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          Не указан ID пользователя
        </div>
        <button
          onClick={() => navigate(-1)}
          className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
        >
          Назад
        </button>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 max-w-4xl mx-auto">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
        <button
          onClick={() => navigate(-1)}
          className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
        >
          Назад
        </button>
      </div>
    );
  }

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Счета пользователя #{user_id}</h1>
        <button
          onClick={() => navigate(-1)}
          className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
        >
          Назад
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full bg-white rounded-lg overflow-hidden">
          <thead className="bg-gray-100">
            <tr>
              <th className="py-3 px-4 text-left">ID</th>
              <th className="py-3 px-4 text-left">Банк</th>
              <th className="py-3 px-4 text-left">Тип</th>
              <th className="py-3 px-4 text-left">Баланс</th>
              <th className="py-3 px-4 text-left">Статус</th>
              <th className="py-3 px-4 text-left">Дата создания</th>
              <th className="py-3 px-4 text-left">Действия</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {accounts.map((account) => (
              <tr key={account.id} className="hover:bg-gray-50">
                <td className="py-3 px-4">{account.id}</td>
                <td className="py-3 px-4">{account.bank_id}</td>
                <td className="py-3 px-4">{getTypeText(account.type)}</td>
                <td className="py-3 px-4">{account.balance} RUB</td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(account.status)}`}>
                    {account.status === 'ON_CONSIDERATION' ? 'НА РАССМОТРЕНИИ' : account.status}
                  </span>
                </td>
                <td className="py-3 px-4">
                  {new Date(account.created_at).toLocaleDateString()}
                </td>
                <td className="py-3 px-4 space-x-2">
                  <button
                    onClick={() => navigate(`/accounts/${account.id}/edit`)}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    Изменить
                  </button>
                  <button
                    onClick={() => navigate(`/accounts/${account.id}/delete`)}
                    className="text-red-600 hover:text-red-800"
                  >
                    Удалить
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {accounts.length === 0 && (
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mt-4">
          У пользователя нет активных счетов
        </div>
      )}
    </div>
  );
};

export default AccountList;