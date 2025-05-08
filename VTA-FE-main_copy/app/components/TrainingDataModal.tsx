import React, { useState } from 'react';
import { CiCircleRemove } from "react-icons/ci";
import { API_BASE_URL } from "@/constants";
import axios from "axios";
import { toast, ToastContainer } from 'react-toastify';

interface TrainingData {
  question: string;
  answer: string;
}

export default function TrainingDataModal({ isOpen }: { isOpen: boolean }) {
  const [trainingData, setTrainingData] = useState<TrainingData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [currentAnswer, setCurrentAnswer] = useState('');

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target?.result as string);
          if (Array.isArray(data)) {
            setTrainingData(data);
            toast.success(`Загружено ${data.length} пар вопросов и ответов`);
          }
        } catch (error) {
          toast.error('Ошибка при чтении файла. Убедитесь, что файл в формате JSON');
        }
      };
      reader.readAsText(file);
    }
  };

  const handleAddPair = () => {
    if (currentQuestion && currentAnswer) {
      setTrainingData([...trainingData, { question: currentQuestion, answer: currentAnswer }]);
      setCurrentQuestion('');
      setCurrentAnswer('');
      toast.success('Пара вопрос-ответ добавлена');
    }
  };

  const handleTrain = async () => {
    if (trainingData.length === 0) {
      toast.error('Нет данных для обучения');
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}vta/train/`, {
        training_data: trainingData
      });
      toast.success('Обучение успешно запущено');
    } catch (error) {
      toast.error('Ошибка при отправке данных на обучение');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = () => {
    const dataStr = JSON.stringify(trainingData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    const exportFileDefaultName = 'training_data.json';

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <div
      className={`sm:w-full md:w-2/3 h-[75vh] main-sec-v2-bg-color absolute top-6 bottom-4 left-[15%] mx-4 m-auto rounded z-10 overflow-y-auto ${
        !isOpen && "hidden"
      }`}
    >
      <div className="flex justify-between px-4 py-3 flex-nowrap items-center border-b border-[#1240AB]/20">
        <h5 className="bot-font tracking-widest text-base font-bold">
          Управление данными для обучения
        </h5>
        <div 
          className="p-2 hover:bg-[#1240AB]/10 hover:scale-110 hover:cursor-pointer rounded-full"
          onClick={() => {/* Добавить функцию закрытия */}}
        >
          <CiCircleRemove size={30} className="text-[#1240AB]" />
        </div>
      </div>

      <div className="px-4 pt-3 text-[#1240AB]">
        <div className="space-y-5">
          {/* Загрузка файла */}
          <div>
            <label className="block text-sm font-medium mb-2">Загрузить данные из файла</label>
            <input
              type="file"
              accept=".json"
              onChange={handleFileUpload}
              className="w-full p-2 border border-[#1240AB]/20 rounded"
            />
          </div>

          {/* Добавление новой пары */}
          <div>
            <label className="block text-sm font-medium mb-2">Добавить новую пару вопрос-ответ</label>
            <textarea
              className="w-full h-20 p-3 rounded bg-white/90 text-sm mb-2"
              placeholder="Введите вопрос..."
              value={currentQuestion}
              onChange={(e) => setCurrentQuestion(e.target.value)}
            />
            <textarea
              className="w-full h-20 p-3 rounded bg-white/90 text-sm mb-2"
              placeholder="Введите ответ..."
              value={currentAnswer}
              onChange={(e) => setCurrentAnswer(e.target.value)}
            />
            <button
              onClick={handleAddPair}
              className="px-6 py-2 bg-[#1240AB] text-white rounded hover:bg-[#1240AB]/90 text-sm"
            >
              Добавить пару
            </button>
          </div>

          {/* Статистика и управление */}
          <div className="border-t border-[#1240AB]/20 pt-3">
            <p className="text-sm mb-2">Загружено пар: {trainingData.length}</p>
            <div className="flex gap-2">
              <button
                onClick={handleTrain}
                disabled={isLoading || trainingData.length === 0}
                className="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600 text-sm disabled:bg-gray-400"
              >
                {isLoading ? 'Обучение...' : 'Начать обучение'}
              </button>
              <button
                onClick={handleExport}
                className="px-6 py-2 bg-[#1240AB] text-white rounded hover:bg-[#1240AB]/90 text-sm"
              >
                Экспорт данных
              </button>
            </div>
          </div>
        </div>
      </div>
      <ToastContainer />
    </div>
  );
} 