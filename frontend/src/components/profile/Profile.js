import { useState, useEffect } from "react";

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  // Состояния для редактирования профиля
  const [updatedName, setUpdatedName] = useState("");
  const [updatedPassportNumber, setUpdatedPassportNumber] = useState("");
  const [updatedEmail, setUpdatedEmail] = useState("");

  // Загрузка профиля
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://localhost:8000/profile", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Ошибка загрузки профиля");
        }

        const data = await response.json();
        setProfile(data);
        setUpdatedName(data.name);
        setUpdatedPassportNumber(data.passport_number);
        setUpdatedEmail(data.email);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  // Обновление профиля
  const handleUpdate = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch("http://localhost:8000/profile", {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: updatedName,
          passport_number: updatedPassportNumber,
          email: updatedEmail,
        }),
      });

      if (!response.ok) {
        throw new Error("Ошибка обновления профиля");
      }

      const data = await response.json();
      setProfile(data);
      setIsEditing(false);
      alert("Профиль успешно обновлен!");
    } catch (err) {
      setError(err.message);
    }
  };

  // Удаление профиля
  const handleDelete = async () => {
    if (window.confirm("Вы уверены, что хотите удалить профиль?")) {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://localhost:8000/profile", {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Ошибка удаления профиля");
        }

        localStorage.removeItem("access_token"); // Удаляем токен
        alert("Профиль успешно удален!");
        window.location.href = "/"; // Перенаправляем на главную страницу
      } catch (err) {
        setError(err.message);
      }
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Профиль</h1>

      {!isEditing ? (
        <div>
          <p><strong>Имя:</strong> {profile.name}</p>
          <p><strong>Номер паспорта:</strong> {profile.passport_number}</p>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Роль:</strong> {profile.role}</p>
          <p><strong>Телефон:</strong> {profile.phone_number}</p>
          <p><strong>Статус:</strong> {profile.is_active ? "Активен" : "Неактивен"}</p>
          <p><strong>Иностранный:</strong> {profile.is_foreign ? "Да" : "Нет"}</p>
          <p><strong>Создан:</strong> {new Date(profile.created_at).toLocaleString()}</p>
          <p><strong>Обновлен:</strong> {new Date(profile.updated_at).toLocaleString()}</p>
          <button
            onClick={() => setIsEditing(true)}
            className="bg-blue-500 text-white p-2 rounded-lg mt-4 hover:bg-blue-600"
          >
            Редактировать профиль
          </button>
        </div>
      ) : (
        <div>
          <div className="mb-4">
            <label htmlFor="name" className="block text-gray-700">Имя</label>
            <input
              type="text"
              id="name"
              value={updatedName}
              onChange={(e) => setUpdatedName(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="passport_number" className="block text-gray-700">Номер паспорта</label>
            <input
              type="text"
              id="passport_number"
              value={updatedPassportNumber}
              onChange={(e) => setUpdatedPassportNumber(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="email" className="block text-gray-700">Email</label>
            <input
              type="email"
              id="email"
              value={updatedEmail}
              onChange={(e) => setUpdatedEmail(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg"
            />
          </div>
          <button
            onClick={handleUpdate}
            className="bg-green-500 text-white p-2 rounded-lg mr-2 hover:bg-green-600"
          >
            Сохранить изменения
          </button>
          <button
            onClick={() => setIsEditing(false)}
            className="bg-gray-500 text-white p-2 rounded-lg hover:bg-gray-600"
          >
            Отмена
          </button>
        </div>
      )}

      <button
        onClick={handleDelete}
        className="bg-red-500 text-white p-2 rounded-lg mt-4 hover:bg-red-600"
      >
        Удалить профиль
      </button>
    </div>
  );
};

export default Profile;