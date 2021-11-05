import DeleteIcon from '@material-ui/icons/Delete';
import { listItem } from './List.scss';

const List = ({ list, handleToggleComplete, handleDelete }) => {
  return (
    <ul>
      {list.map((item) => (

        <li key={item.id}>
          <div className={"listItem"}>

            <span onClick={() => handleToggleComplete(item.id)}
              style={{
                textDecoration: item.is_completed
                  ? 'line-through'
                  : 'none',
              }}
            >
              {item.task}
            </span>
            <div className={"icon"}>
              <DeleteIcon
                onClick={() => handleDelete(item.id)}
              />
            </div>
          </div>
        </li>
      ))
      }
    </ul >
  )
}

export default List