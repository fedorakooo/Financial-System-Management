import { useState } from "react";

const Register = () => {
  const [formData, setFormData] = useState({
    name: "",
    passport_number: "",
    phone_number: "",
    email: "",
    password: "",
    role: "USER",
    is_foreign: false,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userData, setUserData] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setUserData(null);

    try {
      const response = await fetch("http://localhost:8000/registration/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        if (response.status === 409) {
          throw new Error("Пользователь с таким номером уже существует.");
        }
        throw new Error("Ошибка при регистрации. Попробуйте позже.");
      }

      const data = await response.json();
      setUserData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-bold text-center mb-4">Регистрация</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium">Имя</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Паспорт</label>
          <input
            type="text"
            name="passport_number"
            value={formData.passport_number}
            onChange={handleChange}
            required
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Телефон</label>
          <input
            type="text"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            required
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Пароль</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>

        <div className="mb-4 flex items-center">
          <input
            type="checkbox"
            name="is_foreign"
            checked={formData.is_foreign}
            onChange={handleChange}
            className="mr-2"
          />
          <label className="text-sm font-medium">Иностранный пользователь</label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {loading ? "Регистрация..." : "Зарегистрироваться"}
        </button>
      </form>

      {error && <p className="text-red-500 mt-2">{error}</p>}

      {userData && (
        <div className="mt-4 p-4 bg-green-100 rounded">
          <h3 className="font-bold text-lg">Регистрация успешна!</h3>
          <p><strong>ID:</strong> {userData.id}</p>
          <p><strong>Имя:</strong> {userData.name}</p>
          <p><strong>Паспорт:</strong> {userData.passport_number}</p>
          <p><strong>Телефон:</strong> {userData.phone_number}</p>
          <p><strong>Email:</strong> {userData.email}</p>
          <p><strong>Роль:</strong> {userData.role}</p>
          <p><strong>Активен:</strong> {userData.is_active ? "Да" : "Нет"}</p>
          <p><strong>Иностранец:</strong> {userData.is_foreign ? "Да" : "Нет"}</p>
          <p><strong>Создан:</strong> {new Date(userData.created_at).toLocaleString()}</p>
          <p><strong>Обновлен:</strong> {new Date(userData.updated_at).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default Register;
