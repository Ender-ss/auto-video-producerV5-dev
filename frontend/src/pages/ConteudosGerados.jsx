import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { 
  Play, 
  Pause, 
  Eye, 
  Download, 
  Trash2, 
  Search, 
  Calendar, 
  HardDrive, 
  Video, 
  Music, 
  Image, 
  FileText, 
  Volume2,
  Filter,
  Grid,
  List,
  RefreshCw
} from 'lucide-react';
import axios from 'axios';
import VideoPreview from '../components/VideoPreview';

const ConteudosGerados = () => {
  const [content, setContent] = useState({
    text: [],
    images: [],
    audio: [],
    videos: [],
    projects: []
  });
  const [pipelines, setPipelines] = useState([]);
  const [summary, setSummary] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState('list');
  const [selectedType, setSelectedType] = useState('all');
  const [audioControls, setAudioControls] = useState({
    currentAudio: null,
    isPlaying: false,
    currentTime: 0,
    duration: 0
  });

  const audioRef = useRef(null);

  const fetchContent = async () => {
    try {
      setLoading(true);
      const [contentRes, pipelinesRes] = await Promise.all([
        axios.get('http://localhost:5000/api/images/list-all-content'),
        axios.get('http://localhost:5000/api/pipelines/')
      ]);

      setContent(contentRes.data.contents);
      setSummary(contentRes.data.summary);
      setPipelines(pipelinesRes.data);
    } catch (err) {
      setError('Erro ao carregar conteúdo. Verifique se o servidor está rodando.');
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchContent();
  }, []);

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Data não disponível';
    try {
      return format(new Date(dateString), "dd 'de' MMM 'de' yyyy 'às' HH:mm", { locale: ptBR });
    } catch (error) {
      return 'Data inválida';
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'video':
        return <Video className="text-blue-400" size={20} />;
      case 'audio':
        return <Music className="text-green-400" size={20} />;
      case 'image':
        return <Image className="text-purple-400" size={20} />;
      case 'text':
        return <FileText className="text-yellow-400" size={20} />;
      default:
        return <FileText className="text-gray-400" size={20} />;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'video':
        return 'border-blue-500/30';
      case 'audio':
        return 'border-green-500/30';
      case 'image':
        return 'border-purple-500/30';
      case 'text':
        return 'border-yellow-500/30';
      default:
        return 'border-gray-600';
    }
  };

  const getAllContent = () => {
    let allContent = [];
    
    // Adicionar todos os tipos de conteúdo
    if (content.text) {
      allContent = allContent.concat(content.text.map(item => ({...item, type: 'text'})));
    }
    if (content.images) {
      allContent = allContent.concat(content.images.map(item => ({...item, type: 'image'})));
    }
    if (content.audio) {
      allContent = allContent.concat(content.audio.map(item => ({...item, type: 'audio'})));
    }
    if (content.videos) {
      allContent = allContent.concat(content.videos.map(item => ({...item, type: 'video'})));
    }

    // Filtrar por tipo selecionado
    if (selectedType !== 'all') {
      allContent = allContent.filter(item => item.type === selectedType);
    }

    // Filtrar por termo de busca
    if (searchTerm) {
      allContent = allContent.filter(item =>
        item.filename.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Ordenar por data de criação
    return allContent.sort((a, b) => new Date(b.created) - new Date(a.created));
  };

  const handleDownload = async (item) => {
    try {
      let downloadUrl;
      
      // Usar endpoint específico de download para cada tipo de arquivo
      if (item.type === 'image') {
        downloadUrl = `http://localhost:5000/api/images/download/${item.filename}`;
      } else if (item.type === 'audio') {
        downloadUrl = `http://localhost:5000/api/automations/download/audio/${item.filename}`;
      } else if (item.type === 'video') {
        downloadUrl = `http://localhost:5000/api/automations/download/video/${item.filename}`;
      } else if (item.type === 'text') {
        downloadUrl = `http://localhost:5000/api/images/download/text/${item.filename}`;
      } else {
        // Fallback para a URL original
        downloadUrl = `http://localhost:5000${item.url}`;
      }
      
      const response = await axios.get(downloadUrl, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', item.filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Erro ao fazer download do arquivo');
      console.error('Erro:', err);
    }
  };

  const handleDelete = async (item) => {
    if (window.confirm(`Tem certeza que deseja excluir "${item.filename}"?`)) {
      try {
        let url;
        
        // Determinar a URL correta com base no tipo de arquivo e se é de um projeto
        if (item.project_id) {
          // Arquivo de um projeto específico
          url = `http://localhost:5000/api/images/delete/project/${item.project_id}/${item.type}/${item.filename}`;
        } else {
          // Arquivo regular
          url = `http://localhost:5000/api/images/delete/${item.type}/${item.filename}`;
        }
        
        const response = await fetch(url, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
          alert(result.message);
          // Recarregar a lista de conteúdos após a exclusão
          fetchContent();
        } else {
          alert(result.error || 'Erro ao excluir arquivo');
        }
      } catch (err) {
        alert('Erro ao excluir arquivo');
        console.error('Erro:', err);
      }
    }
  };

  const playAudio = (audioUrl) => {
    if (audioRef.current) {
      if (audioControls.currentAudio === audioUrl && audioControls.isPlaying) {
        audioRef.current.pause();
        setAudioControls(prev => ({ ...prev, isPlaying: false }));
      } else {
        audioRef.current.src = `http://localhost:5000${audioUrl}`;
        audioRef.current.play();
        setAudioControls(prev => ({ ...prev, currentAudio: audioUrl, isPlaying: true }));
      }
    }
  };

  const ContentCard = ({ item }) => {
    const [previewUrl, setPreviewUrl] = useState(null);
    const [showPreview, setShowPreview] = useState(false);

    useEffect(() => {
      if (item.type === 'image' || item.type === 'video') {
        setPreviewUrl(`http://localhost:5000${item.url}`);
      }
    }, [item]);

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={`bg-gray-800 rounded-lg border ${getTypeColor(item.type)} p-4 hover:border-gray-500 transition-all`}
      >
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-3">
            {getTypeIcon(item.type)}
            <div>
              <h3 className="text-white font-medium truncate max-w-xs">
                {item.filename}
              </h3>
              <p className="text-gray-400 text-sm capitalize">{item.type}</p>
            </div>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => handleDownload(item)}
              className="text-gray-400 hover:text-white transition-colors"
              title="Download"
            >
              <Download size={16} />
            </button>
            <button
              onClick={() => handleDelete(item)}
              className="text-gray-400 hover:text-red-400 transition-colors"
              title="Excluir"
            >
              <Trash2 size={16} />
            </button>
          </div>
        </div>

        <div className="mb-3">
          {item.type === 'image' && previewUrl && (
            <img 
              src={previewUrl} 
              alt={item.filename}
              className="w-full h-32 object-cover rounded bg-gray-700"
              onClick={() => setShowPreview(true)}
            />
          )}
          {item.type === 'video' && previewUrl && (
            <video 
              src={previewUrl}
              className="w-full h-32 object-cover rounded bg-gray-700"
              controls={false}
              onClick={() => setShowPreview(true)}
            />
          )}
          {item.type === 'audio' && (
            <div className="w-full h-32 bg-gray-700 rounded flex items-center justify-center">
              <Music size={32} className="text-gray-400" />
            </div>
          )}
          {item.type === 'text' && (
            <div className="w-full h-32 bg-gray-700 rounded flex items-center justify-center">
              <FileText size={32} className="text-gray-400" />
            </div>
          )}
        </div>

        <div className="space-y-1 text-sm">
          <div className="flex items-center text-gray-400">
            <HardDrive size={14} className="mr-2" />
            <span>{formatFileSize(item.size)}</span>
          </div>
          <div className="flex items-center text-gray-400">
            <Calendar size={14} className="mr-2" />
            <span>{formatDate(item.created)}</span>
          </div>
        </div>

        {item.type === 'audio' && (
          <button
            onClick={() => playAudio(item.url)}
            className="mt-2 w-full bg-green-600 hover:bg-green-700 text-white py-2 px-3 rounded text-sm flex items-center justify-center"
          >
            {audioControls.currentAudio === item.url && audioControls.isPlaying ? (
              <><Pause size={14} className="mr-2" /> Pausar</>
            ) : (
              <><Play size={14} className="mr-2" /> Reproduzir</>
            )}
          </button>
        )}

        {showPreview && item.type === 'image' && (
          <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" onClick={() => setShowPreview(false)}>
            <img src={previewUrl} alt={item.filename} className="max-w-full max-h-full" />
          </div>
        )}

        {showPreview && item.type === 'video' && (
          <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" onClick={() => setShowPreview(false)}>
            <video src={previewUrl} controls autoPlay className="max-w-full max-h-full" />
          </div>
        )}
      </motion.div>
    );
  };

  const ContentListItem = ({ item }) => {
    return (
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`bg-gray-800 rounded-lg border ${getTypeColor(item.type)} p-4 hover:border-gray-500 transition-all mb-2`}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            {getTypeIcon(item.type)}
            <div>
              <h4 className="text-white font-medium">{item.filename}</h4>
              <p className="text-gray-400 text-sm capitalize">{item.type} • {formatFileSize(item.size)}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <span className="text-gray-400 text-sm">{formatDate(item.created)}</span>
            <div className="flex space-x-2">
              <button
                onClick={() => handleDownload(item)}
                className="text-gray-400 hover:text-white transition-colors"
                title="Download"
              >
                <Download size={16} />
              </button>
              <button
                onClick={() => handleDelete(item)}
                className="text-gray-400 hover:text-red-400 transition-colors"
                title="Excluir"
              >
                <Trash2 size={16} />
              </button>
            </div>
          </div>
        </div>
      </motion.div>
  );
};

const ProjectCard = ({ project }) => {
    const [expanded, setExpanded] = useState(false);
    
    // Contar total de arquivos no projeto
    const totalFiles = 
      (project.contents.text?.length || 0) + 
      (project.contents.images?.length || 0) + 
      (project.contents.audio?.length || 0) + 
      (project.contents.videos?.length || 0);
    
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden"
      >
        <div 
          className="p-4 cursor-pointer flex justify-between items-center"
          onClick={() => setExpanded(!expanded)}
        >
          <div>
            <h3 className="text-white font-medium">Projeto: {project.project_id.substring(0, 8)}...</h3>
            <p className="text-gray-400 text-sm">{totalFiles} arquivos</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="flex space-x-1">
              {project.contents.text && project.contents.text.length > 0 && (
                <FileText className="text-yellow-400" size={16} />
              )}
              {project.contents.images && project.contents.images.length > 0 && (
                <Image className="text-purple-400" size={16} />
              )}
              {project.contents.audio && project.contents.audio.length > 0 && (
                <Music className="text-green-400" size={16} />
              )}
              {project.contents.videos && project.contents.videos.length > 0 && (
                <Video className="text-blue-400" size={16} />
              )}
            </div>
            <motion.div
              animate={{ rotate: expanded ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </motion.div>
          </div>
        </div>
        
        {expanded && (
          <div className="border-t border-gray-700 p-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Textos */}
              {project.contents.text && project.contents.text.length > 0 && (
                <div className="bg-gray-750 rounded-lg p-3">
                  <h4 className="text-white font-medium mb-2 flex items-center">
                    <FileText className="text-yellow-400 mr-2" size={16} />
                    Textos ({project.contents.text.length})
                  </h4>
                  <div className="space-y-2">
                    {project.contents.text.slice(0, 3).map((item, index) => (
                      <div key={index} className="flex justify-between items-center text-sm">
                        <span className="text-gray-300 truncate">{item.filename}</span>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDownload(item);
                          }}
                          className="text-gray-400 hover:text-white"
                        >
                          <Download size={14} />
                        </button>
                      </div>
                    ))}
                    {project.contents.text.length > 3 && (
                      <p className="text-gray-500 text-xs">+{project.contents.text.length - 3} mais</p>
                    )}
                  </div>
                </div>
              )}
              
              {/* Imagens */}
              {project.contents.images && project.contents.images.length > 0 && (
                <div className="bg-gray-750 rounded-lg p-3">
                  <h4 className="text-white font-medium mb-2 flex items-center">
                    <Image className="text-purple-400 mr-2" size={16} />
                    Imagens ({project.contents.images.length})
                  </h4>
                  <div className="grid grid-cols-3 gap-2">
                    {project.contents.images.slice(0, 3).map((item, index) => (
                      <div key={index} className="relative group">
                        <img 
                          src={`http://localhost:5000${item.url}`} 
                          alt={item.filename}
                          className="w-full h-16 object-cover rounded bg-gray-700"
                        />
                        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDownload(item);
                            }}
                            className="text-white"
                          >
                            <Download size={14} />
                          </button>
                        </div>
                      </div>
                    ))}
                    {project.contents.images.length > 3 && (
                      <div className="flex items-center justify-center bg-gray-700 rounded h-16">
                        <span className="text-gray-400 text-xs">+{project.contents.images.length - 3}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              {/* Áudios */}
              {project.contents.audio && project.contents.audio.length > 0 && (
                <div className="bg-gray-750 rounded-lg p-3">
                  <h4 className="text-white font-medium mb-2 flex items-center">
                    <Music className="text-green-400 mr-2" size={16} />
                    Áudios ({project.contents.audio.length})
                  </h4>
                  <div className="space-y-2">
                    {project.contents.audio.slice(0, 3).map((item, index) => (
                      <div key={index} className="flex justify-between items-center text-sm">
                        <span className="text-gray-300 truncate">{item.filename}</span>
                        <div className="flex space-x-1">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              playAudio(item.url);
                            }}
                            className="text-gray-400 hover:text-white"
                          >
                            <Play size={14} />
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDownload(item);
                            }}
                            className="text-gray-400 hover:text-white"
                          >
                            <Download size={14} />
                          </button>
                        </div>
                      </div>
                    ))}
                    {project.contents.audio.length > 3 && (
                      <p className="text-gray-500 text-xs">+{project.contents.audio.length - 3} mais</p>
                    )}
                  </div>
                </div>
              )}
              
              {/* Vídeos */}
              {project.contents.videos && project.contents.videos.length > 0 && (
                <div className="bg-gray-750 rounded-lg p-3">
                  <h4 className="text-white font-medium mb-2 flex items-center">
                    <Video className="text-blue-400 mr-2" size={16} />
                    Vídeos ({project.contents.videos.length})
                  </h4>
                  <div className="space-y-2">
                    {project.contents.videos.slice(0, 3).map((item, index) => (
                      <div key={index} className="flex justify-between items-center text-sm">
                        <span className="text-gray-300 truncate">{item.filename}</span>
                        <div className="flex space-x-1">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDownload(item);
                            }}
                            className="text-gray-400 hover:text-white"
                          >
                            <Download size={14} />
                          </button>
                        </div>
                      </div>
                    ))}
                    {project.contents.videos.length > 3 && (
                      <p className="text-gray-500 text-xs">+{project.contents.videos.length - 3} mais</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </motion.div>
    );
  };

if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Carregando conteúdos...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <button
            onClick={fetchContent}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  const allContent = getAllContent();

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Conteúdos Gerados</h1>
          <p className="text-gray-400">Gerencie todos os seus conteúdos gerados pela IA</p>
        </div>

        {/* Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Textos</p>
                <p className="text-2xl font-bold">{summary.total_text || 0}</p>
              </div>
              <FileText className="text-yellow-400" size={24} />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Imagens</p>
                <p className="text-2xl font-bold">{summary.total_images || 0}</p>
              </div>
              <Image className="text-purple-400" size={24} />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Áudios</p>
                <p className="text-2xl font-bold">{summary.total_audio || 0}</p>
              </div>
              <Music className="text-green-400" size={24} />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Vídeos</p>
                <p className="text-2xl font-bold">{summary.total_videos || 0}</p>
              </div>
              <Video className="text-blue-400" size={24} />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Projetos</p>
                <p className="text-2xl font-bold">{summary.total_projects || 0}</p>
              </div>
              <svg className="text-indigo-400" width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
            </div>
          </div>
        </div>

        {/* Controles */}
        <div className="bg-gray-800 rounded-lg p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-4 items-center">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Buscar conteúdo..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-gray-700 text-white pl-10 pr-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="bg-gray-700 text-white px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">Todos os tipos</option>
                <option value="text">Textos</option>
                <option value="image">Imagens</option>
                <option value="audio">Áudios</option>
                <option value="video">Vídeos</option>
              </select>
              
              <button
                onClick={() => setViewMode(viewMode === 'list' ? 'grid' : 'list')}
                className="bg-gray-700 text-white p-2 rounded-lg hover:bg-gray-600"
              >
                {viewMode === 'list' ? <Grid size={20} /> : <List size={20} />}
              </button>
              
              <button
                onClick={fetchContent}
                className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700"
              >
                <RefreshCw size={20} />
              </button>
            </div>
          </div>
        </div>

        {/* Conteúdo */}
        {allContent.length === 0 && content.projects.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <FileText size={48} className="mx-auto mb-4" />
              <p className="text-xl mb-2">Nenhum conteúdo encontrado</p>
              <p className="text-sm">Execute uma pipeline para gerar conteúdo</p>
            </div>
          </div>
        ) : (
          <div>
            {/* Projetos */}
            {content.projects && content.projects.length > 0 && (
              <div className="mb-8">
                <h2 className="text-xl font-bold mb-4 flex items-center">
                  <svg className="text-indigo-400 mr-2" width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                  </svg>
                  Projetos ({content.projects.length})
                </h2>
                <div className="grid grid-cols-1 gap-4">
                  {content.projects.map((project, index) => (
                    <ProjectCard key={project.project_id} project={project} />
                  ))}
                </div>
              </div>
            )}
            
            {/* Outros conteúdos */}
            {allContent.length > 0 && (
              <div>
                <h2 className="text-xl font-bold mb-4">Outros Conteúdos</h2>
                {viewMode === 'grid' ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    {allContent.map((item, index) => (
                      <ContentCard key={`${item.type}-${index}`} item={item} />
                    ))}
                  </div>
                ) : (
                  <div>
                    {allContent.map((item, index) => (
                      <ContentListItem key={`${item.type}-${index}`} item={item} />
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Áudio Player Oculto */}
        <audio ref={audioRef} />
      </div>
    </div>
  );
};

export default ConteudosGerados;